provider "aws" {
  profile = "default"
  region  = var.aws_region
}

# Selects the most recent official Amazon Linux 2 AMI
data "aws_ami" "amzn2" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
  }

  owners = ["137112412989"] # Amazon
}

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

  # Allow HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
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
  ami           = data.aws_ami.amzn2.id
  instance_type = var.ec2_instance_type
  key_name      = var.ssh_key_pair_name
  security_groups = [
    aws_security_group.docker_host_sg.name
  ]

  connection {
    user        = "ec2-user"
    host        = self.public_ip
    private_key = file(var.ssh_private_key_file)
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install -y docker",
      "sudo systemctl enable docker",
      "sudo systemctl start docker",
      "sudo usermod -a -G docker ec2-user"
    ]
  }
}

resource "null_resource" "deploy_nginx" {
  connection {
    user        = "ec2-user"
    host        = aws_instance.docker_host.public_ip
    private_key = file(var.ssh_private_key_file)
  }

  provisioner "remote-exec" {
    inline = [
      "docker container run -d --name='nginx' --restart=always -p80:80 nginx:latest",
    ]
  }
}
