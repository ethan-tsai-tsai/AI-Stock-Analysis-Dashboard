import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st

def fetch_stock_data(tickers, start_date, end_date):
    stock_data = {}
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date, multi_level_index=False)
        if not data.empty:
            stock_data[ticker] = data
        else:
            st.warning(f"No data found for {ticker}.")
    
    return stock_data
