import streamlit as st
from datetime import datetime, timedelta

def setup_ui():
    # Set Streamlit page configuration
    st.set_page_config(layout='wide')
    st.title('Technical Stock Analysis Dashboard')
    st.sidebar.header("Configuration")

    # Input for stock tickers
    tickers_input = st.sidebar.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, GOOGL")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',') if ticker.strip()]

    # Set the data range: start date and end date
    end_date_default = datetime.now()
    start_date_default = end_date_default - timedelta(days=365)
    start_date = st.sidebar.date_input('Start date', start_date_default)
    end_date = st.sidebar.date_input('End date', end_date_default)

    # Technical indicators selection
    st.sidebar.subheader('Technical Indicators')
    indicators = st.sidebar.multiselect(
        "Select Indicators",
        options=[
            "20-day SMA", "20-Day EMA", "20-Day Bollinger Bands", "VWAP"
        ],
        default=["20-day SMA"]
    )

    return tickers, start_date, end_date, indicators
