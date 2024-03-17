module "Backend" {
  source                    = "./infastructure"
  vpc_id                    = "vpc-00f3eb91a621f7879"
  cluster_name              = "carly-backend-cluster"
  cluster_service_name      = "carly-api-service"
  cluster_service_task_name = "carly-api-task"
  vpc_id_subnet_list        = ["subnet-06b3f30bed04c4cd8", "subnet-0bf7bf07fbf8a2d71", "subnet-0fe50deefaa6c78a8", "subnet-0b31081c793b01a76"]
  execution_role_arn        = "arn:aws:iam::929860961607:role/emz-carly-cicd-role"
  image_id                  = "929860961607.dkr.ecr.eu-central-1.amazonaws.com/carly-backend:latest"
}
