module "Backend" {
  source                    = "./infastructure"
  vpc_id                    = "vpc-0cca3ec5c581a48c3"
  cluster_name              = "carly-backend-cluster"
  cluster_service_name      = "carly-api-service"
  cluster_service_task_name = "carly-api-task"
  vpc_id_subnet_list        = ["subnet-0aa166b83ffd781d9", "subnet-0b8384cf618552502", "subnet-0cfac769babe2908d"]
  execution_role_arn        = "arn:aws:iam::929860961607:role/carly-ecs-role"
  image_id                  = "929860961607.dkr.ecr.eu-central-1.amazonaws.com/carly-backend:latest"
}
