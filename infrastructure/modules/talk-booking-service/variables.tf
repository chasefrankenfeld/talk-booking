variable "region" {
  description = "The AWS region to create resources in."
}

variable "profile" {
  description = "The AWS account to be used"
}

variable "vpc_id" {
  description = "ID od VPC"
  type        = string
}

variable "environment_name" {
  description = "Name of app environment. Must be unique."
  type        = string
}

variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
}

variable "ecs_security_group_id" {
  description = "ID of ECS security group"
  type        = string
}
variable "load_balancer_security_group_id" {
  description = "ID of ALB security group"
  type        = string
}

variable "log_retention_in_days" {
  description = "Log retention in days"
  type        = number
}

variable "public_subnet_1_id" {
  description = "Id of first public subnet"
  type        = string
}

variable "public_subnet_2_id" {
  description = "Id of second public subnet"
  type        = string
}

variable "private_subnet_1_id" {
  description = "Id of first private subnet"
  type        = string
}

variable "private_subnet_2_id" {
  description = "Id of second private subnet"
  type        = string
}

variable "autoscale_min" {
  description = "Minimum autoscale (number of EC2)"
}
variable "autoscale_max" {
  description = "Maximum autoscale (number of EC2)"
}
variable "autoscale_desired" {
  description = "Desired autoscale (number of EC2)"
}

variable "app_count" {
  description = "Desired number of running apps"
  type        = string
}

variable "container_port" {
  description = "App container port"
  type        = number
  default     = 5000
}

variable "app_environment" {
  description = "Application environment"
  type        = string
}
