terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_ecs_task_definition" "pipeline_task" {
  family                   = "c21-george-pipeline-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "pipeline"
      image = var.ECR_IMAGE_URI
      essential = true
      environment = [
        { name = "DB_HOST", value = var.DB_HOST },
        { name = "DB_PORT", value = var.DB_PORT },
        { name = "DB_NAME", value = var.DB_NAME },
        { name = "DB_USER", value = var.DB_USER },
        { name = "DB_PASSWORD", value = var.DB_PASSWORD },
        { name = "AWS_ACCESS_KEY_ID", value = var.AWS_ACCESS_KEY_ID },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.AWS_SECRET_ACCESS_KEY },
        { name = "AWS_DEFAULT_REGION", value = var.AWS_REGION }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/c21-george-pipeline"
          "awslogs-region"        = var.AWS_REGION
          "awslogs-stream-prefix" = "pipeline"
        }
      }
    }
  ])
}

resource "aws_iam_role" "ecs_execution_role" {
  name = "c21-george-pipeline-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_cloudwatch_log_group" "pipeline_logs" {
  name              = "/ecs/c21-george-pipeline"
  retention_in_days = 7
}

resource "aws_iam_role" "scheduler_role" {
  name = "c21-george-pipeline-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "scheduler_policy" {
  name = "c21-george-pipeline-scheduler-policy"
  role = aws_iam_role.scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "ecs:RunTask"
        Resource = "arn:aws:ecs:${var.AWS_REGION}:${var.AWS_ACCOUNT_ID}:task-definition/c21-george-pipeline-task:*"
      },
      {
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = "*"
      }
    ]
  })
}

resource "aws_scheduler_schedule" "pipeline_schedule" {
  name       = "c21-george-pipeline-schedule"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(15 9-21/3 * * ? *)"

  target {
    arn      = "arn:aws:ecs:${var.AWS_REGION}:${var.AWS_ACCOUNT_ID}:cluster/c21-ecs-cluster"
    role_arn = aws_iam_role.scheduler_role.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.pipeline_task.arn
      launch_type         = "FARGATE"

      network_configuration {
        assign_public_ip = true
        subnets          = var.SUBNET_IDS
        security_groups  = var.SECURITY_GROUP_IDS
      }
    }
  }
}