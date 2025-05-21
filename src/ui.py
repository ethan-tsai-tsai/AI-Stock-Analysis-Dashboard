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
            "SMA", "EMA", "Bollinger Bands", "VWAP",
            "RSI", "MACD", "ROC", "CCI"
        ],
        default=["SMA"]
    )

    # Indicator parameters
    indicator_params = {}
    if "SMA" in indicators:
        indicator_params["SMA"] = st.sidebar.number_input("SMA Period", min_value=1, value=20)
    if "EMA" in indicators:
        indicator_params["EMA"] = st.sidebar.number_input("EMA Period", min_value=1, value=20)
    if "Bollinger Bands" in indicators:
        indicator_params["Bollinger_Bands"] = st.sidebar.number_input("Bollinger Bands Period", min_value=1, value=20)
    if "RSI" in indicators:
        indicator_params["RSI"] = st.sidebar.number_input("RSI Period", min_value=1, value=14)
    if "MACD" in indicators:
        indicator_params["MACD_Fast"] = st.sidebar.number_input("MACD Fast Period", min_value=1, value=12)
        indicator_params["MACD_Slow"] = st.sidebar.number_input("MACD Slow Period", min_value=1, value=26)
        indicator_params["MACD_Signal"] = st.sidebar.number_input("MACD Signal Period", min_value=1, value=9)
    if "ROC" in indicators:
        indicator_params["ROC"] = st.sidebar.number_input("ROC Period", min_value=1, value=12)
    if "CCI" in indicators:
        indicator_params["CCI"] = st.sidebar.number_input("CCI Period", min_value=1, value=20)

    return tickers, start_date, end_date, indicators, indicator_params
