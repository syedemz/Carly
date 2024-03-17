

data "aws_vpc" "existing" {
  id = var.vpc_id
}


resource "aws_security_group" "ecs_sg" {
  vpc_id = data.aws_vpc.existing.id
  name   = "ecs-security-group"
  # Inbound and outbound rules
  ingress {
    from_port   = 8890
    to_port     = 8890
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_ecs_task_definition" "task_definition" {
  family                   = var.cluster_service_task_name
  network_mode             = "awsvpc"
  memory                   = "2048"
  requires_compatibilities = ["FARGATE"]


  execution_role_arn = var.execution_role_arn
  task_role_arn      = var.execution_role_arn


  container_definitions = jsonencode([
    {
      name   = "flask-api-container"
      image  = var.image_id
      cpu    = 1024
      memory = 2048
      port_mappings = [
        {
          container_port = 8890
          host_port      = 8890
          protocol       = "tcp"
        }
      ],
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "carly-backend"
          awslogs-region        = "eu-central-1"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  cpu = "1024"
}


resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.cluster_name
}

resource "aws_ecs_service" "service" {
  name            = var.cluster_service_name
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [var.vpc_id_subnet_list[0], var.vpc_id_subnet_list[1], var.vpc_id_subnet_list[2]]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.server_target_group.arn
    container_name   = "flask-api-container"
    container_port   = 8890
  }
}
