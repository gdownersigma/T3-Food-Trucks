"""Chart functions for the Culinary Experience Dashboard."""
import altair as alt
import pandas as pd


def fsa_rating_by_truck_chart(df: pd.DataFrame) -> alt.Chart:
    """Bar chart showing FSA rating for each truck."""
    fsa_by_truck = df.groupby('truck_name')['fsa_rating'].mean().reset_index()
    fsa_by_truck.columns = ['truck_name', 'fsa_rating']

    chart = alt.Chart(fsa_by_truck).mark_bar().encode(
        x=alt.X('fsa_rating', title='FSA Rating',
                scale=alt.Scale(domain=[0, 5])),
        y=alt.Y('truck_name', sort='-x', title='Truck'),
    ).properties(height=300)

    return chart


def revenue_by_fsa_rating_chart(df: pd.DataFrame) -> alt.Chart:
    """Bar chart showing total revenue by FSA rating."""
    revenue_by_fsa = df.groupby('fsa_rating')['total'].sum().reset_index()
    revenue_by_fsa.columns = ['fsa_rating', 'revenue']

    chart = alt.Chart(revenue_by_fsa).mark_bar().encode(
        x=alt.X('fsa_rating:O', title='FSA Rating'),
        y=alt.Y('revenue', title='Revenue (£)')
    ).properties(height=300)

    return chart


def transactions_by_fsa_rating_chart(df: pd.DataFrame) -> alt.Chart:
    """Bar chart showing transaction count by FSA rating."""
    transactions_by_fsa = df.groupby(
        'fsa_rating').size().reset_index(name='transactions')

    chart = alt.Chart(transactions_by_fsa).mark_bar().encode(
        x=alt.X('fsa_rating:O', title='FSA Rating'),
        y=alt.Y('transactions', title='Transactions')
    ).properties(height=300)

    return chart


def card_reader_pie_chart(df: pd.DataFrame) -> alt.Chart:
    """Pie chart showing trucks with/without card readers."""
    # Get unique trucks with their card reader status
    truck_card_reader = df.groupby('truck_name')[
        'has_card_reader'].first().reset_index()
    card_reader_counts = truck_card_reader['has_card_reader'].value_counts(
    ).reset_index()
    card_reader_counts.columns = ['has_card_reader', 'count']
    card_reader_counts['has_card_reader'] = card_reader_counts['has_card_reader'].map({
                                                                                      True: 'Yes', False: 'No'})

    chart = alt.Chart(card_reader_counts).mark_arc().encode(
        theta='count',
        color=alt.Color('has_card_reader', title='Has Card Reader')
    ).properties(height=300)

    return chart
