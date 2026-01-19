# T3 Pipeline ECS Deployment

This Terraform configuration deploys the T3 food truck ETL pipeline to AWS ECS.

## What it creates

- ECS Task Definition for running the pipeline
- IAM roles and policies for ECS execution
- CloudWatch Log Group for container logs
- EventBridge Schedule to run the pipeline every 3 hours

## Prerequisites

- AWS CLI configured
- Terraform installed
- Docker image pushed to ECR

## Setup

1. Create a `terraform.tfvars` file with your values:
```
AWS_REGION            = "eu-west-2"
AWS_ACCESS_KEY_ID     = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_ACCOUNT_ID        = "your_account_id"
ECR_IMAGE_URI         = "your_ecr_uri/c21-george-live-trucks:latest"
DB_HOST               = "your_db_host"
DB_PORT               = "3306"
DB_NAME               = "your_db_name"
DB_USER               = "your_db_user"
DB_PASSWORD           = "your_db_password"
SUBNET_IDS            = ["subnet-xxxxx"]
SECURITY_GROUP_IDS    = ["sg-xxxxx"]
```

2. Initialise Terraform:
```bash
terraform init
```

3. Deploy:
```bash
terraform plan
terraform apply
```

## Running the task manually

1. Go to AWS Console → ECS → Task definitions
2. Select `c21-george-pipeline-task`
3. Click Deploy → Run task
4. Select cluster, Fargate launch type, and networking
5. Click Create

## Viewing logs

1. Go to AWS Console → CloudWatch → Log groups
2. Select `/ecs/c21-george-pipeline`
3. View the log streams for each task run

## Schedule

The pipeline runs automatically at 9:15, 12:15, 15:15, 18:15, and 21:15 daily via EventBridge Scheduler.