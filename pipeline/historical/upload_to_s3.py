"""Script to upload parquet files to S3."""

import awswrangler as wr
import os
from dotenv import load_dotenv


def upload_to_s3(local_dir: str, bucket: str, prefix: str = "") -> None:
    """Upload local parquet files to S3, preserving folder structure."""
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".parquet"):
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)

                s3_path = (
                    f"s3://{bucket}/{prefix}/{relative_path}"
                    if prefix
                    else f"s3://{bucket}/{relative_path}"
                )

                wr.s3.upload(
                    local_file=local_path,
                    path=s3_path
                )
                print(f"Uploaded {local_path} to {s3_path}")


if __name__ == "__main__":
    load_dotenv()

    bucket_name = "c21-george-food-truck"

    # Upload transaction parquet files (time-partitioned by truck)
    upload_to_s3("data/input/transaction", bucket_name, "input/transaction")

    # Upload dimension tables
    upload_to_s3("data/input/truck", bucket_name, "input/truck")
    upload_to_s3("data/input/payment_method",
                 bucket_name, "input/payment_method")

    print("All uploads complete!")
