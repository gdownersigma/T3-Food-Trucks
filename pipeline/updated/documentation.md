# T3 Food Truck ETL Pipeline

This pipeline extracts transaction data from the T3 RDS database, transforms it, converts it to parquet format, and uploads it to S3.

## Prerequisites

- Python 3.12
- AWS credentials with access to the S3 bucket and RDS
- Access to the T3 RDS database

## Setup

1. Create a virtual environment:
```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
   DB_HOST=your_database_host
   DB_PORT=3306
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_DEFAULT_REGION=eu-west-2
```

## Running the Pipeline
```bash
python pipeline.py
```

The pipeline will:
1. Extract transactions from the last 3 hours from RDS
2. Transform and clean the data
3. Create time-partitioned parquet files
4. Upload to S3