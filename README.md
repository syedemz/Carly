# The project components are described as follows

Github Repo : This repo contains all the associated code with this project.
The code/carly_server folder contains all the python files including the flask server and the associated files
The code/infastructure folder contains all the terraform files for AWS infastructure deployment
The code/tests contains all the unit test files

Github Actions: The repository is configured with github actions, the associated yml file can be found in the .github/workflows folder, as soon as a push is made to the main branch of this repo, or a Pull Request is merged with the main branch, this triggers a CICD pipeline which installs dependencies, builds a docker image and uploads it into an AWS ECR repository. All of these steps can be investigated in the aforementioned yml file

Terraform: Github actions then initiates the terraform environment and the infastructure is deployed to AWS.

Once the cicd pipeline finishes, the docker image is pulled from ECR and deployed to an ECS Fargate service. The service is integrated with an AWS elastic load balancer which provides a DNS name at which the server can be reached, The ALB itself is hooked up to an API Gateway, this allows for the possibility of adding further security layers such as lambda authorizers.

All the customer info is stored into a dynamoDB table.

The server endpoints are secured by using JWT tokens, endpoints '/changepassword' and '/changelanguage' can only be reached one you have successfully logged in, Furthermore, all the endpoints are accessible only if the provided client version number in the request headers is higher than 2.1.0.

An architectural diagram has been provided for ease of understanding.

The customer_importer_dynamo.py file was implemented to load the customer info provided into a dynamodb table
