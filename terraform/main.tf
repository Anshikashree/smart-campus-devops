terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = var.aws_region }
variable "aws_region" { type = string; default = "ap-south-1" }
variable "ami_id" { type = string; description = "Ubuntu AMI ID for the selected region" }
variable "key_name" { type = string; description = "Existing EC2 key pair name" }
variable "my_ip_cidr" { type = string; description = "Your public IPv4 address in CIDR form, e.g. 203.0.113.5/32" }
resource "aws_security_group" "campus" {
  name = "smart-campus-demo-sg"
  description = "Demo access for Smart Campus"
  ingress { from_port = 22; to_port = 22; protocol = "tcp"; cidr_blocks = [var.my_ip_cidr] }
  ingress { from_port = 5000; to_port = 5000; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  egress { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
  tags = { Name = "smart-campus-demo-sg" }
}
resource "aws_instance" "campus" {
  ami = var.ami_id
  instance_type = "t2.micro"
  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.campus.id]
  tags = { Name = "SmartCampusDemo" }
}
output "instance_public_ip" { value = aws_instance.campus.public_ip }
