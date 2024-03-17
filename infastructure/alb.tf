
resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.carly_application_load_balancer.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.server_target_group.arn
  }
}


resource "aws_lb_target_group" "server_target_group" {
  name        = "carly-target-group"
  port        = 8890
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = data.aws_vpc.existing.id
  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 10
    interval            = 30
  }
}


resource "aws_alb" "carly_application_load_balancer" {
  name               = "carly-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [var.vpc_id_subnet_list[0], var.vpc_id_subnet_list[1], var.vpc_id_subnet_list[2]]
  # define this security group
  security_groups = [aws_security_group.alb_sg.id]
}


resource "aws_security_group" "alb_sg" {
  vpc_id                 = data.aws_vpc.existing.id
  name                   = "carly-sg-alb"
  description            = "Security group for alb"
  revoke_rules_on_delete = true
}

resource "aws_security_group_rule" "alb_http_ingress" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "TCP"
  description       = "Allow http inbound traffic from internet"
  security_group_id = aws_security_group.alb_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}
resource "aws_security_group_rule" "alb_https_ingress" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "TCP"
  description       = "Allow https inbound traffic from internet"
  security_group_id = aws_security_group.alb_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "alb_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  description       = "Allow outbound traffic from alb"
  security_group_id = aws_security_group.alb_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}
