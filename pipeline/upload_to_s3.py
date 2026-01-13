"""Script to upload parquet files to S3."""

import awswrangler as wr
import os


def upload_to_s3(local_dir: str, bucket: str, prefix: str = "") -> None:
    """Upload local parquet files to S3, preserving the folder structure."""
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".parquet"):
                local_path = os.path.join(root, file)

                relative_path = os.path.relpath(local_path, local_dir)

                s3_path = f"s3://{bucket}/{prefix}/{relative_path}" if prefix else f"s3://{bucket}/{relative_path}"

                wr.s3.upload(local_path, s3_path)
                print(f"Uploaded {local_path} to {s3_path}")


if __name__ == "__main__":
    bucket_name = "c21-george-food-truck"
    local_directory = "data"
    s3_prefix = "transactions"

    upload_to_s3(local_directory, bucket_name, s3_prefix)
