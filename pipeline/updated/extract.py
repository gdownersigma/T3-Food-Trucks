"""Script to download data from the RDS and save it locally."""
from os import environ as ENV
import pymysql
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta


def get_conn() -> pymysql.connections.Connection:
    """Establish a connection to the RDS database."""
    conn = pymysql.connect(
        host=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        port=int(ENV["DB_PORT"])
    )
    return conn


def extract_data(table: str, conn: pymysql.connections.Connection) -> pd.DataFrame:
    """Extract data from all tables in the database if it is less than 3 hours old."""
    if table == "FACT_Transaction":
        since = (datetime.now() - timedelta(hours=3)
                 ).strftime('%Y-%m-%d %H:%M:%S')
        query = f"SELECT * FROM {table} WHERE at > '{since}';"
    else:
        query = f"SELECT * FROM {table};"
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    load_dotenv()
    conn = get_conn()
    tables = ["DIM_Truck", "FACT_Transaction", "DIM_Payment_Method"]
    for table in tables:
        df = extract_data(table, conn)
        df.to_csv(f"data/{table}.csv", index=False)
    conn.close()
