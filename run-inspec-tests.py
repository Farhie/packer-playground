import json
import os
from random import randint
import subprocess
import boto3
import time
from botocore.exceptions import ClientError


def generate_private_key(ec2_client):
    private_key_filename = 'temporary-key-{}.pem'.format(randint(10000, 10000000))
    ec2_key_pair_name = 'packer-key-pair-{}'.format(randint(10000, 10000000))
    response = ec2_client.create_key_pair(KeyName=ec2_key_pair_name)
    file = open(private_key_filename, 'w')
    file.write(response['KeyMaterial'])
    file.close()
    os.chmod(private_key_filename, 400)
    return ec2_key_pair_name, private_key_filename


def clean_up_keys(ec2_client, ec2_key_pair_name, private_key_filename):
    if os.path.isfile(private_key_filename):
        os.remove(private_key_filename)
    if ec2_key_pair_name is not None:
        ec2_client.delete_key_pair(KeyName=ec2_key_pair_name)


def ssh_ingress_security_group(ec2_client):
    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        group_name = 'allow_ssh_ingress_for_inspec_testing_{}'.format(randint(10000, 10000000))
        response = ec2_client.create_security_group(GroupName=group_name,
                                                    Description='Inspec requires SSH access to run tests',
                                                    VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
        return security_group_id, group_name
    except ClientError as e:
        print(e)


def wait_for_status_checks_to_pass(ec2, instance):
    while True:
        statuses = ec2.describe_instance_status(InstanceIds=[instance.instance_id], IncludeAllInstances=True)
        status = statuses['InstanceStatuses'][0]
        if status['InstanceStatus']['Status'] == 'ok' and status['SystemStatus']['Status'] == 'ok':
            print('InstanceStatuses are ok. sshd will be available.')
            break
        print('InstanceStatus: {}, SystemStatus: {}. Waiting for InstanceStatuses to be OK'
              .format(status['InstanceStatus']['Status'], status['SystemStatus']['Status']))
        time.sleep(5)


def main():
    ec2 = instance = security_group_id = security_group_name = ec2_key_pair_name = private_key_filename = None
    region = "us-west-1"
    ami_id = json.load(open('packer-image.json'))['ami_id']
    print("Running Inspec tests on AMI: {}".format(ami_id))
    try:
        ec2 = boto3.client('ec2')
        ec2_key_pair_name, private_key_filename = generate_private_key(ec2)
        ec2_resource = boto3.resource('ec2')
        security_group_id, security_group_name = ssh_ingress_security_group(ec2)

        instance = ec2_resource.create_instances(ImageId=ami_id,
                                                 MinCount=1,
                                                 MaxCount=1,
                                                 InstanceType='t2.micro',
                                                 SecurityGroupIds=[security_group_id],
                                                 KeyName=ec2_key_pair_name)[0]
        wait_for_status_checks_to_pass(ec2, instance)
        print("Instance: {} running. sshd should not be running.".format(instance.instance_id))
        instance.reload()
        print("Public IP address: {} ".format(instance.public_ip_address))

        subprocess.run(['inspec', 'exec', 'spec/',
                        '-t', 'ssh://ec2-user@{}'.format(instance.public_ip_address),
                        '-i', private_key_filename],
                       check=True)
        print('Tests completed. Cleaning up.')
    finally:
        if ec2_key_pair_name is not None:
            clean_up_keys(ec2, ec2_key_pair_name, private_key_filename)
            print('Keypair used for testing deleted.')
        if instance is not None:
            print('Terminating instance used for testing.')
            instance.terminate()
            instance.wait_until_terminated()
            print('Terminated.')
        if security_group_id is not None:
            ec2.delete_security_group(GroupId=security_group_id, GroupName=security_group_name)
            print('Deleted security group that allows ssh ingress for Inspec.')


if __name__ == "__main__":
    main()
