from random import randint

import boto3
import subprocess

key_name = 'packer-key-pair-{}'.format(randint(10000, 1000000000000000))
private_key_filename = '{}.pem'.format(key_name)

ec2 = boto3.client('ec2')
response = ec2.create_key_pair(KeyName=key_name)
private_key = response['KeyMaterial']

f = open(private_key_filename, 'w')
f.write(private_key)
f.close()

subprocess.run(['chmod', '400', private_key_filename])

subprocess.run(['packer', 'build', '-var', 'private_key={}'.format(private_key_filename),
                '-var', 'instance_user={}'.format(key_name), 'amazon-linux.json'], check=True)

ec2.delete_key_pair(KeyName=key_name)
