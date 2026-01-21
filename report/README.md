# T3 Daily Report Lambda Function

This directory contains the Lambda function that generates daily HTML reports from T3 (food truck) transaction data.

## Overview

The Lambda function (`report.py`) queries yesterday's transactions from AWS Athena, calculates summary statistics, and generates an HTML report. It is deployed as a containerized Lambda function through Terraform.

## Function Details

### Purpose

- Queries Athena for transaction data from the previous day
- Calculates summary statistics (total revenue, transaction count, per-truck breakdown)
- Generates an HTML report with formatted tables and styling
- Outputs report as an HTML file

### Key Functions

- `get_yesterday_date()`: Returns yesterday's date in YYYY-MM-DD format
- `load_yesterday_data(database)`: Queries Athena for yesterday's transactions
- `calculate_summary(df)`: Computes summary statistics
- `generate_html(summary)`: Creates formatted HTML report
- `save_report(html, filename)`: Writes report to file
- `handler(event, context)`: Lambda entry point

## Running the Lambda Function

### Option 1: Run Locally (for testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script directly
python3 report.py
```

This will generate a report file named `report_YYYY-MM-DD.html`.

### Option 2: Deploy and Invoke via AWS Console

1. **Deploy to AWS:**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Invoke the Lambda function:**
   - Go to AWS Lambda console
   - Find function: `c21-george-daily-report`
   - Click "Test"
   - Use empty test event: `{}`
   - Click "Invoke"

### Option 3: Invoke via AWS CLI

```bash
aws lambda invoke \
  --function-name c21-george-daily-report \
  --region eu-west-2 \
  response.json
```


## Environment Variables

The function requires AWS credentials to be configured:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

These should be set in a `.env` file or configured through AWS IAM roles when deployed to Lambda.

## Infrastructure

The Lambda function is deployed via Terraform with:

- **Function Name:** `c21-george-daily-report`
- **Container Image:** Stored in ECR (`c21-george-t3-report:latest`)
- **Timeout:** 300 seconds (5 minutes)
- **Memory:** 512 MB
- **Region:** eu-west-2
- **IAM Permissions:** S3, Glue, Athena, CloudWatch Logs

### Terraform Files

- `terraform/main.tf`: Lambda function, IAM roles, and Athena/S3 permissions
- `terraform/variables.tf`: Variable definitions
- `terraform/terraform.tfvars`: AWS credentials and configuration values

## Dependencies

See `requirements.txt` for Python package dependencies.

Key packages:
- `awswrangler`: AWS data querying and S3 integration
- `python-dotenv`: Environment variable management
