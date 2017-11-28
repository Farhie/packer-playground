## Hardened AMIs

### Purpose
The [Center for Internet Security (CIS)](https://www.cisecurity.org/) provide 
[benchmarks](https://www.cisecurity.org/cis-benchmarks/) for hardening a variety of 
operating systems and software packages. This repo provides a workflow to facilitate
the creation of CIS compliant Amazon Linux Machines Images (AMIs).

### Tools 
* [Ansible](https://www.ansible.com/) is used to configure the machine images
* [Packer](https://www.packer.io/) is used to produce the AMIs
* [Inspec](inspec.io) is used to provide an automated way of verifying compliance

### Assumptions
* You have an AWS account with appropriate permissions

### Prerequisites 
* [Install Packer](https://www.packer.io/docs/install/index.html) (confirmed working with 1.1.2)
* [Install Ruby](https://www.ruby-lang.org/en/documentation/installation/) (confirmed working with 2.4.2)
* [Install Inspec](https://github.com/chef/inspec) (Confirmed working with 1.45.9)
* [Install Python3](https://www.python.org/downloads/) (confirmed working with 3.6.3)
* [Install Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html) (confirmed working with 2.4.1.0)
* Get Python dependencies: `pip3 install -r requirements.txt`


### Creating an AMI
* To build an image run `python3 build-packer-image.py`
* Packer will bring up an EC2 instance with the AMI specified in the script
* Then the Ansible contained in `packer-ansible` will be run against the instance
* A snapshot is then taken
* The AMI ID is outputted to a file called `packer-image.json`

### Testing an AMI
* To test the created image run `python3 run-inspec-tests.py`
* Creates a security group that allows SSH ingress
* Brings up a new instance with the AMI ID found in `packer-image.json` and a temporary key pair
* Runs the Inspec tests
* Cleans up the instance, security group and keypair.
