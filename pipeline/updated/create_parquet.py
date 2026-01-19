"""Script to create time-partitioned parquet files from a dataframe."""
import pandas as pd
import os
from datetime import datetime


def prep_for_partition(df: pd.DataFrame) -> pd.DataFrame:
    """Add partition columns (year, month, day) to the dataframe."""
    df = df.copy()
    df['at'] = pd.to_datetime(df['at'])

    df['year'] = df['at'].dt.year
    df['month'] = df['at'].dt.month
    df['day'] = df['at'].dt.day

    return df


def load_from_csv(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file (for standalone use only)."""
    return pd.read_csv(file_path)


def save_as_parquet(df: pd.DataFrame) -> None:
    """Create time-partitioned parquet files for each truck."""

    for (truck, year, month, day), group in df.groupby(['truck_name', 'year', 'month', 'day']):
        # Sanitise truck name for folder (replace spaces, special chars)
        truck_folder = truck.replace(' ', '_').replace("'", "")

        folder_path = f"data/input/transaction/{truck_folder}/year={year}/month={month:02d}/day={day:02d}"
        os.makedirs(folder_path, exist_ok=True)

        group = group.drop(columns=['year', 'month', 'day'])

        min_id = group['transaction_id'].min()
        max_id = group['transaction_id'].max()
        file_path = os.path.join(
            folder_path, f"transactions_{min_id}_{max_id}.parquet")
        group.to_parquet(file_path, index=False)
        print(f"Saved {file_path} with {len(group)} records.")


if __name__ == "__main__":
    df = load_from_csv("data/clean_transactions.csv")
    df = prep_for_partition(df)
    save_as_parquet(df)
