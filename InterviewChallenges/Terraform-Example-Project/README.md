# Terraform Example Project


## Challenge Description

The goal of this project is to use Terraform to create an EC2 instance in AWS,
install Docker on that EC2 instance, then run an Nginx container on the newly
created Docker host. The Terraform scripts must be as self-contained as
possible. This repository contains the scripts that were used to complete the
challenge, as well as document the steps that were followed to create the docker
host and run the container.


## External Dependencies

The Terraform script in this repository is not completely self-contained. The
script depends on a pre-existing SSH keypair in the targeted AWS account, which
must be referenced using the `ssh_key_pair_name` variable. The private key file
must also exist on the local machine and must be referenced using the
`ssh_private_key_file` variable. This repository contains an "ssh-keys.tfvars"
file that has default settings for those 2 pieces of information, which can be
used as a guide for configuring and setting up those variables.

If you correctly set up

- an SSH key pair in AWS EC2 named "aws-ec2-key-pair"
- an SSH private key file named and located at `~/.ssh/aws-ec2-key-pair.pem`

you'll be able to apply this example using

```bash
terraform apply -var-file=ssh-keys.tfvars
```


## Steps Followed to Complete the Challenge

### Terraform Installation

Terraform is packaged and distributed as a zip archive, so installation is
slightly more involved than `sudo apt install terraform`. The download links for
various architectures and operating systems are located at the link below.

https://www.terraform.io/downloads.html

For my setup, (Ubuntu 19.10), I downloaded the Linux x64 Zip and unpacked it
into `~/.local/bin`, which is referenced by my PATH.


```bash
sha256sum ~/Downloads/terraform_0.12.20_linux_amd64.zip
# 46bd906f8cb9bbb871905ecb23ae7344af8017d214d735fbb6d6c8e0feb20ff3
unzip ~/Downloads/terraform_0.12.20_linux_amd64.zip -d ~/.local/bin
which terraform
# /home/austin/.local/bin/terraform
terraform -v
# Terraform v0.12.20
```


### Getting Started

This example project roughly follows the example project for setting up an AWS
EC2 instance. The start of that learning module can be found at the link below.

https://learn.hashicorp.com/terraform/getting-started/build

Our project will focus on installing Docker CE on an AWS EC2 instance, so we can
run a container based on the `nginx` Docker container image.


### AWS and EC2 Configuration

To start, we need to make sure that we have AWS auth credentials stored at
`~/.aws/credentials`. This can be achieved by either creating the file and
populating it manually, or by installing the AWS CLI and running
`aws configure`, which allows you to copy and paste your credentials into the
terminal window.

Since we will be installing Docker on an EC2 instance, we need to make sure that
the AMI and Instance Type that we choose are compatible with Docker, both in
terms of hardware and OS requirements. Based on AWS docs, it appears that Amazon
Linux 2 supports installing Docker. Not sure which version of Docker we'll get
at this point, but it's supported in general and we have official installation
instructions from AWS. I can't find any official word on Docker CE's minimum
system requirements, but apparently it can run with as little as 512MBs of RAM
on a Raspberry PI, so we should be fine to use the "free-tier eligible"
`t2.micro`.

**AWS Amazon Linux Docker Docs:**

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html

**Selected AMI:**

- `ami-0a887e401f7654935`
- Amazon Linux 2
- 64-bit x86

**Selected Instance Type:**

- `t2.micro`
- General purpose
- 1 vCPU	
- 1 GiB RAM


### Applying a Deployment

Now that we have selected our AMI and Instance Type for this project, we can
write a `*.tf` file, which defines what we will be deploying to AWS.

```terraform
provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0a887e401f7654935"
  instance_type = "t2.micro"
}
```

To launch this on AWS, we need to run `terraform init` using the Terraform CLI
to initialize settings, data, and download plugins, then run `terraform apply`
to instruct Terraform to create the requested resources. We can also verify our
Terraform configuration using `terraform validate`.

```bash
terraform init
# ...
# Terraform has been successfully initialized!
# ...

terraform validate
# Success! The configuration is valid.

terraform apply
# Do you want to perform these actions?
#  Terraform will perform the actions described above.
#  Only 'yes' will be accepted to approve.
#
#  Enter a value: yes
```


### Gitignore

The first test showed that in addition to creating resources in our selected
cloud platform, terraform creates a `.terraform` directory after running
`terraform init` and updates a `*.tfstate` file after running `terraform apply`.
Looking at these files, they probably should not be checked into source-control,
especially not to a publicly accessible repository.

Since we're only about 10 minutes in, I'm sure there will be more files that we
will need to exclude from the Git repository. I typically take this opportunity
to check https://github.com/github/gitignore to see if someone has already
created a decent gitignore that I can copy.

```bash
curl https://raw.githubusercontent.com/github/gitignore/master/Terraform.gitignore >> .gitignore
git add .gitignore
git commit -m 'Updated the .gitignore with settings for Terraform'
```


### Provisioning

An empty EC2 isn't much use to anyone except the AWS finance department. Since
our selected AMI does not have Docker installed, we need to use a "Provisioner"
to initialize the EC2 resource. Provisioners can be added to resources by
including them in the resource declaration.

```terraform
resource "aws_instance" "example" {
  ami           = "ami-0a887e401f7654935 "
  instance_type = "t2.micro"
  provisioner "local-exec" {
    command = "echo ${aws_instance.example.public_ip} > ip_address.txt"
  }
}
```

Provisioners Documentation: https://www.terraform.io/docs/provisioners/

The docs for provisioners explicitly state:

> **Provisioners are a Last Resort**
> 
> Terraform includes the concept of provisioners as a measure of pragmatism,
> knowing that there will always be certain behaviors that can't be directly
> represented in Terraform's declarative model.

If "install docker on Amazon Linux 2" is a common deployment, it would be a good
idea to create a VM image that has docker installed.


### Installing Docker

> The `remote-exec` provisioner invokes a script on a remote resource after it
> is created. This can be used to run a configuration management tool, bootstrap
> into a cluster, etc. To invoke a local process, see the local-exec provisioner
> instead. The `remote-exec` provisioner supports both ssh and winrm type
> connections.

Converting the docs for installing Docker on Amazon Linux 2 to a `remote-exec`
provisioner yields this new resource declaration:

```terraform
resource "aws_instance" "example" {
  ami           = "ami-0a887e401f7654935"
  instance_type = "t2.micro"
  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install docker",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
    ]
  }
}
```


### Configuring SSH Keys for an EC2 Resource

AWS EC2 has a feature that allows you to create SSH key pairs for EC2 instances.
The UI for creating those pairs can be found by going to the EC2 service and
selecting "Key Pairs". From here, you can create a new key pair with a unique
name that you can associate with EC2 instances. Once you've done that, AWS will
prompt you to download the private key file (a `.pem` file) to your local file
system.

You can then reference the name of the key-pair when creating EC2 resources
using Terraform. If you need to authenticate any provisioners with the EC2
resource, you can reference the local private-key file when configuring SSH
connections.

```terraform
resource "aws_instance" "example" {
  # ...
  key_name = "aws-ec2-key-pair"
  connection {
    user = "ubuntu"
    host = self.public_ip
    private_key = file("~/.ssh/aws-ec2-key-pair.pem")
  }
  # ...
}
```


### Selecting the Most Recent AMZN2 AMI

It's possible to query the available AWS EC2 AMIs within Terraform. This allows
terraform to select an appropriate VM image without hard-coding the AMI into the
source files. This also allowing future deployments to automatically use updated
versions of compatible Linux images.

```terraform
data "aws_ami" "amzn2" {
  most_recent = true

  filter {
    name = "name"
    values = ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
  }

  owners = ["137112412989"] # Amazon
}

resource "aws_instance" "example" {
  ami = data.aws_ami.amzn2.id
  # ...
```


### Specifying a Security Group

Up until now, we have been relying on the default security group's configuration
settings when launching new AWS EC2 instances. We should codify the security
configuration of the EC2 instance so that we are not relying on the current
state of the default security group of our AWS account.

```terraform
# Specifies a new security group for the Docker host machine 
resource "aws_security_group" "docker_host_sg" {
  name = "docker_host_sg"

  # Allow access to SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outgoing traffic to anywhere.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "docker_host" {
  # ...
  security_groups = [aws_security_group.docker_host_sg.name]
  # ...
}
```


### Deploying a Container to our Docker Host

If we had a more stable Docker host we could use the "docker" provider which
would allow us to provision container instances on a remote Docker host using
Terraform syntax. Unfortunately, since we are also creating the Docker host in
this step, it is not possible to reference the IP address of the newly created
AWS EC2 instance within the "docker" provider.

**Docker Provider Docs:** https://www.terraform.io/docs/providers/docker/index.html

**Limitation of Providers:** https://github.com/hashicorp/terraform/issues/2430

We can instead use the "null_resource" provider to execute arbitrary bash
statements on the remote host over SSH. Again, the Terraform docs mention that
provisioners should be used as a "last resort", so keep this in mind if you are
deploying containers in a production context. It would be much wiser to use the
"docker_container" resource type, but that would require either multiple calls
to `terraform apply` or a more complicated long-term configuration such as
setting up an ECS or an EKS.

```terraform
resource "null_resource" "deploy_nginx" {
  connection {
    user        = "ec2-user"
    host        = aws_instance.docker_host.public_ip
    private_key = file("~/.ssh/aws-ec2-key-pair.pem")
  }

  provisioner "remote-exec" {
    inline = [
      "docker container run -d -p80:80 nginx:latest",
    ]
  }
}
```

This will run a single replica of an nginx container on the remote host by
running the docker CLI on the remote host. It's worth noting at this step that
we need to configure the container so it exposes its port 80 as port 80 on the
host machine, so we should update the security group accordingly.

```terraform
resource "aws_security_group" "docker_host_sg" {
  name = "docker_host_sg"
  # ...
  # Allow HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # ...
}
```


### Variables

We should do some light refactoring to make future configuration easier. A good
way to start would be to break out some of the plaintext strings into variables
that can be overridden, such as the following pieces of information:

- SSH Key-Pair Identifiers
- EC2 Instance Type
- AWS Region
