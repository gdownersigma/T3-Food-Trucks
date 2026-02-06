# Pipeline

This folder contains the ETL pipeline that processes food truck transaction data from an RDS database and uploads it to S3 in a partitioned format.

## How It Works

The pipeline runs a 4-step ETL process:

1. **Extract** (`extract.py`)
   - Connects to the RDS database using credentials from environment variables
   - Extracts transaction data from the last 3 hours
   - Loads dimension tables (trucks and payment methods)

2. **Transform** (`transform.py`)
   - Merges transactions with truck and payment method data
   - Cleans the data (standardizes payment methods, strips whitespace)
   - Removes any invalid or incomplete records

3. **Create Parquet** (`create_parquet.py`)
   - Adds partition columns (year, month, day) based on transaction timestamp
   - Converts the data to parquet format
   - Organizes files by truck name and date hierarchy

4. **Upload to S3** (`upload_to_s3.py`)
   - Uploads the partitioned parquet files to S3
   - Preserves the folder structure: `transaction/{truck_name}/year={year}/month={month}/day={day}/`

## Running the Pipeline

The main entry point is `pipeline.py` which orchestrates all steps:

```bash
python pipeline.py
```

## Infrastructure

- **Terraform** (`terraform/`) - Manages AWS resources (S3 buckets, Glue crawler, database)
- **Streamlit** (`streamlit/`) - Dashboard for visualizing the data
- **Dockerfile** - Containerises the pipeline for deployment