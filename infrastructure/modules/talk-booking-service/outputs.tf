output "load_balancer_dns" {
  value = aws_lb.load_balancer.dns_name
}

output "ecr_url" {
  value = aws_ecr_repository.talk-booking.repository_url
}
