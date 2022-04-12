resource "aws_lb" "load_balancer" {
  name               = "${var.environment_name}-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [var.load_balancer_security_group_id]
  subnets            = [var.public_subnet_1_id, var.public_subnet_2_id]
}

# Target group client
resource "aws_alb_target_group" "default-target-group" {
  name       = "${var.environment_name}-client-tg"
  port       = 80
  protocol   = "HTTP"
  vpc_id     = var.vpc_id
  depends_on = [aws_lb.load_balancer]

  health_check {
    path                = "/health-check/"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 5
    matcher             = "200"
  }
}

# Target group users
resource "aws_alb_target_group" "users-target-group" {
  name     = "${var.environment_name}-users-tg"
  port     = var.container_port
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/health-check/"
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 5
    matcher             = "200"
  }
}

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_alb_listener" "ecs-alb-http-listener" {
  load_balancer_arn = aws_lb.load_balancer.id
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.default-target-group]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.default-target-group.arn
  }
}
