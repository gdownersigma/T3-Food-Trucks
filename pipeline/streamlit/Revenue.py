"""Revenue Dashboard for food truck transaction and revenue analysis."""
import pandas as pd
import streamlit as st

from chart import (
    revenue_by_truck_chart,
    daily_revenue_trend_chart,
    payment_method_pie_chart,
    revenue_by_hour_chart,
)
from load import load_data


st.set_page_config(page_title="T3 Food Truck Dashboard", layout="wide")


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters for truck selection and date range."""
    st.sidebar.header("Filters & Pages")

    # Truck filter (multiselect)
    selected_trucks = st.sidebar.multiselect(
        "Trucks", df['truck_name'].unique())
    if selected_trucks:
        df = df[df['truck_name'].isin(selected_trucks)]

    # Date range filter
    df['date'] = pd.to_datetime(df['at']).dt.date
    min_date = df['date'].min()
    max_date = df['date'].max()

    start_date = st.sidebar.date_input(
        "Start Date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input(
        "End Date", value=max_date, min_value=min_date, max_value=max_date)

    # Apply date filter
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    return df


def display_kpis(df: pd.DataFrame) -> None:
    """Display key performance indicators for revenue metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_revenue = df['total'].sum()
        st.metric("Total Revenue", f"£{total_revenue:,.0f}")

    with col2:
        total_transactions = len(df)
        st.metric("Total Transactions", f"{total_transactions:,}")

    with col3:
        avg_transaction = df['total'].mean()
        st.metric("Avg Transaction", f"£{avg_transaction:,.2f}")

    with col4:
        total_trucks = df['truck_name'].nunique()
        st.metric("Total Trucks", total_trucks)


def display_charts(df: pd.DataFrame) -> None:
    """Display revenue-related charts in a two-column layout."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Truck")
        st.altair_chart(revenue_by_truck_chart(df), use_container_width=True)

        st.subheader("Daily Revenue Trend")
        st.altair_chart(daily_revenue_trend_chart(df),
                        use_container_width=True)

    with col2:
        st.subheader("Revenue by Payment Method")
        st.altair_chart(payment_method_pie_chart(df), use_container_width=True)

        st.subheader("Transactions by Hour")
        st.altair_chart(revenue_by_hour_chart(df), use_container_width=True)


def main() -> None:
    """Main function to run the Revenue Dashboard."""
    st.title("Revenue Dashboard")

    df = load_data()
    df = apply_sidebar_filters(df)
    display_kpis(df)
    display_charts(df)


if __name__ == "__main__":
    main()
