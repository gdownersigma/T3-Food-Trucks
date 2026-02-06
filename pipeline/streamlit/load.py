"""Data loading module for Streamlit dashboard."""
import awswrangler as wr
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load transaction data from Athena."""
    load_dotenv()
    df = wr.athena.read_sql_query(
        sql="SELECT * FROM input",
        database="c21-george-food-truck",
        workgroup="primary"
    )
    df['total'] = df['total'] / 100  # Convert pence to pounds
    return df


if __name__ == "__main__":
    df = load_data()
    print(f"Loaded {len(df)} records from Athena.")
