# T3 Food Truck Data Platform

A data platform for processing and analysing food truck transaction data. The system extracts data from an RDS database, transforms it into a queryable format, and provides dashboards for business insights.

## Architecture

```
┌─────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│  RDS MySQL  │ -> │ ETL Pipeline  │ -> │  S3 Bucket  │ -> │ AWS Athena   │
└─────────────┘    └───────────────┘    └─────────────┘    └──────────────┘
                                                                   │
                                                                   v
                                              ┌─────────────────────────────┐
                                              │  Streamlit Dashboard        │
                                              │  + Daily Report Lambda      │
                                              └─────────────────────────────┘
```

## Project Structure

| Directory | Description |
|-----------|-------------|
| `pipeline/` | ETL pipeline for extracting, transforming, and loading data |
| `pipeline/historical/` | Full historical data load |
| `pipeline/updated/` | Incremental updates (last 3 hours) |
| `pipeline/streamlit/` | Interactive dashboards for data visualisation |
| `pipeline/terraform/` | Infrastructure as code for AWS resources |
| `report/` | Lambda function for generating daily HTML reports |

## Getting Started

### Prerequisites

- Python 3.10+
- AWS credentials configured
- Access to the T3 RDS database

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r pipeline/requirements.txt
```

### Environment Variables

Create a `.env` file with the following:

```
DB_HOST=your-rds-host
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database
DB_PORT=3306
```

### Running the Pipeline

```bash
cd pipeline/updated
python pipeline.py
```

### Running the Dashboard

```bash
cd pipeline/streamlit
streamlit run Revenue.py
```

## Features

- **Revenue Dashboard**: Track total revenue, transactions, and performance by truck
- **Culinary Dashboard**: Monitor FSA ratings and food safety metrics
- **Daily Reports**: Automated HTML reports delivered via Lambda
- **Time-Partitioned Storage**: Efficient querying with Hive-style partitions

## Infrastructure

Infrastructure is managed with Terraform. See `pipeline/terraform/` for S3, Glue, and Athena resources.

```bash
cd pipeline/terraform
terraform init
terraform apply
```
