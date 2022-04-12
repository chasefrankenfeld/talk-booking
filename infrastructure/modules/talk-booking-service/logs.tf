resource "aws_cloudwatch_log_group" "talk-booking-log-group" {
  name              = "/ecs/${var.environment_name}"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_stream" "talk-booking-log-stream" {
  name           = "${var.environment_name}-app-log-stream"
  log_group_name = aws_cloudwatch_log_group.talk-booking-log-group.name
}
