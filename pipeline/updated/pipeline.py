"""Main pipeline script that runs the full ETL process."""
from extract import get_conn, extract_data
from transform import merge_data, clean_data
from create_parquet import save_as_parquet, prep_for_partition
from upload_to_s3 import upload_to_s3
from dotenv import load_dotenv
import shutil
import os


def run_pipeline():
    """Run the full ETL pipeline, passing dataframes directly between steps."""
    load_dotenv()

    # Clear local data folder
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data", exist_ok=True)

    # Step 1: Extract from RDS (keep as dataframes)
    print("Step 1: Extracting data from RDS...")
    conn = get_conn()
    trucks = extract_data("DIM_Truck", conn)
    transactions = extract_data("FACT_Transaction", conn)
    payments = extract_data("DIM_Payment_Method", conn)
    conn.close()
    print(
        f"Extracted {len(transactions)} transactions, {len(trucks)} trucks, {len(payments)} payment methods.")

    if len(transactions) == 0:
        print("No new transactions to process. Exiting pipeline.")
        return

    # Step 2: Transform/clean the data (dataframes passed directly)
    print("Step 2: Transforming data...")
    df = merge_data(trucks, transactions, payments)
    print(f"Merged into {len(df)} rows.")

    df = clean_data(df)
    print(f"Cleaned to {len(df)} rows.")

    # Step 3: Create parquet files (dataframe passed directly)
    print("Step 3: Creating parquet files...")
    df_partitioned = prep_for_partition(df)
    save_as_parquet(df_partitioned)

    # Step 4: Upload to S3
    print("Step 4: Uploading to S3...")
    bucket_name = "c21-george-food-truck"

    # Upload transaction parquet files (time-partitioned by truck)
    upload_to_s3("data/input/transaction", bucket_name, "input/transaction")

    # Upload dimension tables
    upload_to_s3("data/input/truck", bucket_name, "input/truck")
    upload_to_s3("data/input/payment_method",
                 bucket_name, "input/payment_method")

    print("All uploads complete!")

    print("Pipeline complete!")


if __name__ == "__main__":
    run_pipeline()
