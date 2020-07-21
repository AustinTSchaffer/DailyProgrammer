variable "ssh_key_pair_name" {
  description = "The key name to use for the instance."
  type        = string
}

variable "ssh_private_key_file" {
  description = "The file name and path of the SSH private key file."
  type        = string
}

variable "ec2_instance_type" {
  description = "The type of instance to start"
  type        = string
  default     = "t2.micro"
}

variable "aws_region" {
  description = "The region where the EC2 instance should be deployed."
  type        = string
  default     = "us-east-1"
}
