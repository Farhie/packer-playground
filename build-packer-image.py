from random import randint
from retrying import retry
import boto3
import subprocess
import json


def retry_if_index_error(exception):
    return isinstance(exception, IndexError)


@retry(retry_on_exception=retry_if_index_error, wait_fixed=3000, stop_max_attempt_number=10)
def get_id_of_packer_created_ami(ami_name, ec2_client):
    print("Attempting to get AMI's with name={}\n".format(ami_name))
    images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': [ami_name]}])
    return images['Images'][0]['ImageId']


def packer_build(ec2_client, region):
    ami_name = "packer-amazon-linux-{}".format(randint(10000, 1000000000000000))
    subprocess.run(['packer', 'build',
                    '-var', 'ami_name={}'.format(ami_name),
                    '-var', 'region={}'.format(region),
                    'amazon-linux.json'], check=True)
    return get_id_of_packer_created_ami(ami_name, ec2_client)


def output_to_json_file(ami_id):
    file = open('packer-image.json', 'w')
    file.write(json.dumps(dict([('ami_id', ami_id)])))
    file.close()


def main():
    ec2_client = boto3.client('ec2')
    region = "us-west-1"
    ami_id = packer_build(ec2_client, region)
    output_to_json_file(ami_id)


if __name__ == "__main__":
    main()
