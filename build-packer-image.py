from random import randint
from retrying import retry
import boto3
import subprocess
import json

import os


def generate_private_key(ec2_client, private_key_filename, ec2_key_pair_name):
    response = ec2_client.create_key_pair(KeyName=ec2_key_pair_name)
    file = open(private_key_filename, 'w')
    file.write(response['KeyMaterial'])
    file.close()
    os.chmod(private_key_filename, 400)


def retry_if_index_error(exception):
    return isinstance(exception, IndexError)


@retry(retry_on_exception=retry_if_index_error, wait_fixed=3000, stop_max_attempt_number=10)
def get_id_of_packer_created_ami(ami_name, ec2_client):
    print("Attempting to get AMI's with name={}\n".format(ami_name))
    images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': [ami_name]}])
    return images['Images'][0]['ImageId']


def packer_build(private_key_filename, ec2_key_pair_name, ec2_client, region):
    ami_name = "packer-amazon-linux-{}".format(randint(10000, 1000000000000000))
    subprocess.run(['packer', 'build', '-var', 'private_key_location={}'.format(private_key_filename),
                    '-var', 'ec2_key_pair_name={}'.format(ec2_key_pair_name),
                    '-var', 'ami_name={}'.format(ami_name), '-var', 'region={}'.format(region),
                    'amazon-linux.json'], check=True)
    return get_id_of_packer_created_ami(ami_name, ec2_client)


def output_to_file(ami_id, ec2_key_pair_name):
    file = open('packer-image.json', 'w')
    file.write(json.dumps(dict([('ami_id', ami_id), ('ec2_key_pair_name', ec2_key_pair_name)])))
    file.close()


def main():
    ec2_client = boto3.client('ec2')
    private_key_filename = 'temporary-key-{}.pem'.format(randint(10000, 1000000000000000))
    ec2_key_pair_name = 'packer-key-pair-{}'.format(randint(10000, 1000000000000000))
    region = "us-west-1"
    generate_private_key(ec2_client, private_key_filename, ec2_key_pair_name)
    ami_id = packer_build(private_key_filename, ec2_key_pair_name, ec2_client, region)
    output_to_file(ami_id, ec2_key_pair_name)


if __name__ == "__main__":
    main()
