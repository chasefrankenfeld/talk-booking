resource "aws_db_subnet_group" "main" {
  name       = var.environment_name
  subnet_ids = [var.private_subnet_1_id, var.private_subnet_2_id]
}

resource "random_password" "db_password" {
  length           = 35
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_security_group" "rds" {
  name        = var.environment_name
  description = "Allows inbound access from ECS only"
  vpc_id      = var.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    security_groups = [var.ecs_security_group_id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "talk_booking" {
  identifier              = var.environment_name
  name                    = "app"
  username                = "app"
  password                = random_password.db_password.result
  port                    = "5432"
  engine                  = "postgres"
  engine_version          = "12.5"
  instance_class          = "db.t3.micro"
  allocated_storage       = "20"
  storage_encrypted       = false
  vpc_security_group_ids  = [aws_security_group.rds.id]
  db_subnet_group_name    = aws_db_subnet_group.main.name
  multi_az                = false
  storage_type            = "gp2"
  publicly_accessible     = false
  backup_retention_period = 7
  skip_final_snapshot     = true
}

resource "aws_secretsmanager_secret" "db_connection_string" {
  name                    = "db-connection-string-${var.app_environment}"
  description             = "Database connection string"
  recovery_window_in_days = 14
}

resource "aws_secretsmanager_secret_version" "db_connection_string" {
  secret_id     = aws_secretsmanager_secret.db_connection_string.id
  secret_string = "postgresql://${aws_db_instance.talk_booking.username}:${random_password.db_password.result}@${aws_db_instance.talk_booking.endpoint}/${aws_db_instance.talk_booking.name}"
}
