resource "aws_ecs_task_definition" "app" {
  family                = "${var.environment_name}-app"
  container_definitions = <<EOF
[
    {
      "name": "talk-booking-app",
      "image": "${aws_ecr_repository.talk-booking.repository_url}:latest",
      "cpu": 1000,
      "command": [
        "gunicorn",
        "--bind",
        "0.0.0.0:${var.container_port}",
        "web_app.main:app",
        "-k",
        "uvicorn.workers.UvicornWorker"
      ],
      "memory": 950,
      "essential": true,
      "environment": [
        {"name": "APP_ENVIRONMENT", "value": "${var.app_environment}"},
        {"name": "AWS_DEFAULT_REGION", "value": "${var.region}"}
      ],
      "portMappings": [
        {
          "containerPort": ${var.container_port}
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${aws_cloudwatch_log_group.talk-booking-log-group.name}",
          "awslogs-region": "${var.region}",
          "awslogs-stream-prefix": "${aws_cloudwatch_log_stream.talk-booking-log-stream.name}"
        }
      }
    }
]
EOF
  lifecycle {
    ignore_changes = all
  }
}

resource "aws_ecs_service" "talk-booking-service" {
  name                               = var.environment_name
  cluster                            = aws_ecs_cluster.talk-booking-cluster.name
  task_definition                    = aws_ecs_task_definition.app.family
  iam_role                           = aws_iam_role.ecs-service-role.arn
  desired_count                      = var.app_count
  deployment_minimum_healthy_percent = 50

  load_balancer {
    target_group_arn = aws_alb_target_group.default-target-group.arn
    container_name   = "talk-booking-app"
    container_port   = var.container_port
  }
  depends_on = [aws_alb_listener.ecs-alb-http-listener]

  lifecycle {
    ignore_changes = [task_definition]
  }
}
