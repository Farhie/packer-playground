from random import randint

import boto3
import subprocess

import os


def generate_private_key(ec2_client, ec2_key_pair_name, private_key_filename):
    response = ec2_client.create_key_pair(KeyName=ec2_key_pair_name)
    f = open(private_key_filename, 'w')
    f.write(response['KeyMaterial'])
    f.close()
    os.chmod(private_key_filename, 400)


def packer_build(private_key_filename, ec2_key_pair_name):
    subprocess.run(['packer', 'build', '-var', 'private_key_location={}'.format(private_key_filename),
                    '-var', 'ec2_key_pair_name={}'.format(ec2_key_pair_name), 'amazon-linux.json'], check=True)


def main():
    ec2_client = boto3.client('ec2')
    ec2_key_pair_name = 'packer-key-pair-{}'.format(randint(10000, 1000000000000000))
    private_key_filename = 'temporary_key.pem'
    try:
        generate_private_key(ec2_client, ec2_key_pair_name, private_key_filename)
        packer_build(private_key_filename, ec2_key_pair_name)
    finally:
        ec2_client.delete_key_pair(KeyName=ec2_key_pair_name)
        os.remove(private_key_filename)


if __name__ == "__main__":
    main()
