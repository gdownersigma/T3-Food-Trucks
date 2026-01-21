"""Script to generate daily HTML report from yesterday's transactions."""
import awswrangler as wr
from datetime import datetime, timedelta
from dotenv import load_dotenv


def get_yesterday_date() -> str:
    """Get yesterday's date as a string."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def load_yesterday_data(database: str):
    """Query Athena for yesterday's transaction data."""
    yesterday = get_yesterday_date()

    query = f"""
        SELECT * FROM input
        WHERE CAST(from_unixtime(at / 1000000000) AS DATE) = DATE '{yesterday}'
    """

    df = wr.athena.read_sql_query(
        query,
        database=database,
        workgroup="primary"
    )

    return df


def calculate_summary(df) -> dict:
    """Calculate summary statistics from the data."""
    summary = {
        'date': get_yesterday_date(),
        'total_revenue': df['total'].sum(),
        'total_transactions': len(df),
        'avg_transaction': df['total'].mean(),
        'revenue_by_truck': df.groupby('truck_name')['total'].sum().to_dict(),
        'transactions_by_truck': df.groupby('truck_name').size().to_dict()
    }
    return summary


def generate_html(summary: dict) -> str:
    """Generate HTML report from summary data."""
    html = f"""
    <html>
    <head>
        <title>T3 Daily Report - {summary['date']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>T3 Daily Report</h1>
        <h2>{summary['date']}</h2>
        
        <h2>Summary</h2>
        <p><strong>Total Revenue:</strong> £{summary['total_revenue']:,.2f}</p>
        <p><strong>Total Transactions:</strong> {summary['total_transactions']}</p>
        <p><strong>Average Transaction:</strong> £{summary['avg_transaction']:,.2f}</p>
        
        <h2>Revenue by Truck</h2>
        <table>
            <tr><th>Truck</th><th>Revenue</th><th>Transactions</th></tr>
    """

    for truck, revenue in sorted(summary['revenue_by_truck'].items(), key=lambda x: x[1], reverse=True):
        transactions = summary['transactions_by_truck'].get(truck, 0)
        html += f"<tr><td>{truck}</td><td>£{revenue:,.2f}</td><td>{transactions}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html


def save_report(html: str, filename: str) -> None:
    """Save HTML report to file."""
    with open(filename, 'w') as f:
        f.write(html)
    print(f"Report saved to {filename}")


def handler(event=None, context=None):
    """Lambda handler function."""
    if event is None:
        event = {}

    print("Loading yesterday's data from Athena...")
    df = load_yesterday_data("c21-george-food-truck")
    print(f"Loaded {len(df)} transactions")

    print("Calculating summary...")
    summary = calculate_summary(df)

    print("Generating HTML report...")
    html = generate_html(summary)

    return {
        'statusCode': 200,
        'body': html,
        'headers': {'Content-Type': 'text/html'}
    }


if __name__ == "__main__":
    load_dotenv()

    print(handler())
