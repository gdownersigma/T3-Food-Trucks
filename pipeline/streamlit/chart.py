"""Script to create altair charts for Streamlit dashboard."""

import altair as alt
import pandas as pd


def revenue_by_truck_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a bar chart of revenue by truck."""
    revenue_by_truck = df.groupby('truck_name')['total'].sum().reset_index()
    revenue_by_truck.columns = ['truck_name', 'revenue']

    chart = alt.Chart(revenue_by_truck).mark_bar().encode(
        x=alt.X('revenue', title='Revenue (£)'),
        y=alt.Y('truck_name', sort='-x', title='Truck')
    ).properties(height=300)
    return chart


def daily_revenue_trend_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a line chart of daily revenue trend."""
    df['date'] = pd.to_datetime(df['at']).dt.strftime('%Y-%m-%d')
    daily_revenue = df.groupby('date')['total'].sum().reset_index()
    daily_revenue.columns = ['date', 'revenue']

    chart = alt.Chart(daily_revenue).mark_line().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('revenue', title='Revenue (£)')
    ).properties(height=300)
    return chart


def payment_method_pie_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a pie chart of revenue by payment method."""
    revenue_by_payment = df.groupby('payment_method')[
        'total'].sum().reset_index()
    revenue_by_payment.columns = ['payment_method', 'revenue']

    chart = alt.Chart(revenue_by_payment).mark_arc().encode(
        theta='revenue',
        color='payment_method'
    ).properties(height=300)
    return chart


def revenue_by_hour_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a bar chart of revenue by hour."""
    df['hour'] = pd.to_datetime(df['at']).dt.hour
    revenue_by_hour = df.groupby('hour')['total'].sum().reset_index()
    revenue_by_hour.columns = ['hour', 'revenue']

    chart = alt.Chart(revenue_by_hour).mark_bar().encode(
        x=alt.X('hour:O', title='Hour of Day'),
        y=alt.Y('revenue', title='Revenue (£)')
    ).properties(height=300)
    return chart
