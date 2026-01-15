"""Culinary Experience Dashboard for food truck FSA ratings and metrics."""
from load import load_data
from culinary_charts import (
    fsa_rating_by_truck_chart,
    revenue_by_fsa_rating_chart,
    transactions_by_fsa_rating_chart,
    card_reader_pie_chart,
)
import streamlit as st
import pandas as pd
import sys
sys.path.insert(0, '..')


st.set_page_config(page_title="Culinary Dashboard", layout="wide")


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters for truck selection and date range."""
    st.sidebar.header("Filters")

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
    """Display key performance indicators for culinary metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_fsa = df['fsa_rating'].mean()
        st.metric("Avg FSA Rating", f"{avg_fsa:.1f}")

    with col2:
        total_trucks = df['truck_name'].nunique()
        st.metric("Total Trucks", total_trucks)

    with col3:
        best_truck = df.groupby('truck_name')['fsa_rating'].mean().idxmax()
        st.metric("Highest Rated", best_truck)

    with col4:
        worst_truck = df.groupby('truck_name')['fsa_rating'].mean().idxmin()
        st.metric("Lowest Rated", worst_truck)


def display_charts(df: pd.DataFrame) -> None:
    """Display culinary-related charts in a two-column layout."""
    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("FSA Rating by Truck")
        st.altair_chart(fsa_rating_by_truck_chart(df),
                        use_container_width=True)

    with col2:
        st.subheader("Revenue by FSA Rating")
        st.altair_chart(revenue_by_fsa_rating_chart(df),
                        use_container_width=True)

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transactions by FSA Rating")
        st.altair_chart(transactions_by_fsa_rating_chart(df),
                        use_container_width=True)

    with col2:
        st.subheader("Card Reader Availability")
        st.altair_chart(card_reader_pie_chart(df), use_container_width=True)


def main() -> None:
    """Main function to run the Culinary Experience Dashboard."""
    st.title("Culinary Experience Dashboard")

    df = load_data()
    df = apply_sidebar_filters(df)
    display_kpis(df)
    display_charts(df)


if __name__ == "__main__":
    main()
