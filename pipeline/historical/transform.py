"""Script to clean and transform the extracted data."""
import pandas as pd


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the extracted CSV files."""
    trucks = pd.read_csv("data/DIM_Truck.csv")
    transactions = pd.read_csv("data/FACT_Transaction.csv")
    payments = pd.read_csv("data/DIM_Payment_Method.csv")
    return trucks, transactions, payments


def merge_data(trucks: pd.DataFrame, transactions: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    """Merge all tables into one denormalised dataset."""
    df = transactions.merge(trucks, on="truck_id", how="left")
    df = df.merge(payments, on="payment_method_id", how="left")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the merged dataset."""
    # Convert datetime column
    df['at'] = pd.to_datetime(df['at'])

    # Strip whitespace from text columns
    df['truck_name'] = df['truck_name'].str.strip()
    df['truck_description'] = df['truck_description'].str.strip()
    df['payment_method'] = df['payment_method'].str.strip()

    # Standardise payment method to title case
    df['payment_method'] = df['payment_method'].str.title()

    # Convert has_card_reader to boolean
    df['has_card_reader'] = df['has_card_reader'].astype(bool)

    # Drop duplicate transactions
    df = df.drop_duplicates(subset=['transaction_id'])

    # Drop rows with missing essential values
    df = df.dropna(subset=['transaction_id', 'truck_id', 'total'])

    # Select and reorder columns
    df = df[[
        'transaction_id',
        'at',
        'truck_name',
        'truck_description',
        'has_card_reader',
        'fsa_rating',
        'payment_method',
        'total'
    ]]

    # Sort by transaction time
    df = df.sort_values('at')

    return df


if __name__ == "__main__":
    trucks, transactions, payments = load_data()
    print(
        f"Loaded {len(transactions)} transactions, {len(trucks)} trucks, {len(payments)} payment methods.")

    df = merge_data(trucks, transactions, payments)
    print(f"Merged into {len(df)} rows.")

    df = clean_data(df)
    print(f"Cleaned to {len(df)} rows.")

    df.to_csv("data/clean_transactions.csv", index=False)
    print("Saved to data/clean_transactions.csv")
