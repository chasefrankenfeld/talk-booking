resource "aws_ecr_repository" "talk-booking" {
  name                 = var.environment_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
