variable "region" {
  description = "The AWS region to create resources in."
  default     = "eu-west-1"
}

variable "profile" {
  description = "The AWS account to be used."
  default     = "chase"
}

variable "vpc_state_username" {
  type = string
  description = "Username to access VPC's terraform state"
}
variable "vpc_state_password" {
  type = string
  sensitive = true
  description = "Password to access VPC's terraform state"
}
