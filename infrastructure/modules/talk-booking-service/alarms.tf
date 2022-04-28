resource "aws_sns_topic" "alarm_sns" {
  name = "alarm-topic-${var.environment_name}"
}

resource "aws_sns_topic_subscription" "email_alarms" {
  topic_arn = aws_sns_topic.alarm_sns.arn
  protocol  = "email"
  endpoint  = "chasefrankenfeld@gmail.com"
}

resource "aws_cloudwatch_metric_alarm" "alb_average_response_time" {
  alarm_name          = "average-response-time-${var.environment_name}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "TargetResponseTime"
  namespace           = "AWS/NetworkELB"
  period              = "300"
  statistic           = "Average"
  threshold           = 1
  alarm_description   = "Average response time over 5 minutes"
  actions_enabled     = "true"
  alarm_actions       = [aws_sns_topic.alarm_sns.arn]
  dimensions = {
    TargetGroup  = aws_alb_target_group.default-target-group.arn_suffix
    LoadBalancer = aws_lb.load_balancer.arn_suffix
  }
}
