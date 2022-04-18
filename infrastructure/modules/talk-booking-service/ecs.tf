data "aws_ami" "ecs-ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-2.0.20220328-*"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_ecs_cluster" "talk-booking-cluster" {
  name = var.environment_name
}

resource "aws_launch_configuration" "ecs" {
  name                        = var.environment_name
  image_id                    = data.aws_ami.ecs-ami.id
  instance_type               = var.instance_type
  security_groups             = [var.ecs_security_group_id]
  iam_instance_profile        = aws_iam_instance_profile.ecs.name
  associate_public_ip_address = true
  user_data                   = "#!/bin/bash\necho ECS_CLUSTER=${aws_ecs_cluster.talk-booking-cluster.name} >> /etc/ecs/ecs.config"
}

resource "aws_autoscaling_group" "ecs-cluster" {
  name                 = "${var.environment_name}-auto-scaling-group"
  min_size             = var.autoscale_min
  max_size             = var.autoscale_max
  desired_capacity     = var.autoscale_desired
  health_check_type    = "EC2"
  launch_configuration = aws_launch_configuration.ecs.name
  vpc_zone_identifier  = [var.private_subnet_1_id, var.private_subnet_2_id]
}
