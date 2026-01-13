"""Main pipeline script that runs the full ETL process."""
from extract import get_conn, extract_data
from transform import load_data, merge_data, clean_data
from create_parquet import save_as_parquet, prep_for_partition
from upload_to_s3 import upload_to_s3
from dotenv import load_dotenv


def run_pipeline():
    load_dotenv()

    # Step 1: Extract from RDS
    print("Step 1: Extracting data from RDS...")
    conn = get_conn()
    tables = ["DIM_Truck", "FACT_Transaction", "DIM_Payment_Method"]
    for table in tables:
        df = extract_data(table, conn)
        df.to_csv(f"data/{table}.csv", index=False)
    conn.close()

    # Step 2: Transform/clean the data
    print("Step 2: Transforming data...")
    trucks, transactions, payments = load_data()
    print(
        f"Loaded {len(transactions)} transactions, {len(trucks)} trucks, {len(payments)} payment methods.")

    df = merge_data(trucks, transactions, payments)
    print(f"Merged into {len(df)} rows.")

    df = clean_data(df)
    print(f"Cleaned to {len(df)} rows.")
    df.to_csv("data/clean_transactions.csv", index=False)
    print("Saved to data/clean_transactions.csv")

    # Step 3: Create parquet files
    print("Step 3: Creating parquet files...")
    save_as_parquet(prep_for_partition("data/clean_transactions.csv"))

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
