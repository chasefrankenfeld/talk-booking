output "load_balancer_dns" {
  value = module.talk-booking-service.load_balancer_dns
}

output "ecr_url" {
  value = module.talk-booking-service.ecr_url
}
