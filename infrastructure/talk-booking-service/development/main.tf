terraform {
  backend "http" {}
}

provider "aws" {
  region = var.region
}
data "terraform_remote_state" "vpc" {
  backend = "http"

  # the number in "projects/35320676/*" is the Gitlab ProjectID from the repo
  config = {
    address  = "https://gitlab.com/api/v4/projects/35320676/terraform/state/vpc"
    username = var.vpc_state_username
    password = var.vpc_state_password
  }
}

module "talk-booking-service" {
  source = "../../modules/talk-booking-service"

  vpc_id                          = data.terraform_remote_state.vpc.outputs.vpc_id
  ecs_security_group_id           = data.terraform_remote_state.vpc.outputs.ecs_security_group_id
  load_balancer_security_group_id = data.terraform_remote_state.vpc.outputs.load_balancer_security_group_id
  public_subnet_1_id              = data.terraform_remote_state.vpc.outputs.public_subnet_1_id
  public_subnet_2_id              = data.terraform_remote_state.vpc.outputs.public_subnet_2_id
  private_subnet_1_id             = data.terraform_remote_state.vpc.outputs.private_subnet_1_id
  private_subnet_2_id             = data.terraform_remote_state.vpc.outputs.private_subnet_2_id
  instance_type                   = "t3.small"
  log_retention_in_days           = 30
  autoscale_min                   = 1
  autoscale_desired               = 1
  autoscale_max                   = 4
  region                          = var.region
  app_count                       = 1
  environment_name                = "talk-booking-dev"
  app_environment                 = "development"
  domain_zone_id                  = data.terraform_remote_state.vpc.outputs.domain_zone_id
  domain                          = "development.beerlibrary.co"
}
