import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st

def fetch_stock_data(tickers, start_date, end_date, market="US Stocks"):
    stock_data = {}
    for ticker in tickers:
        # Add .TW suffix for Taiwan stocks
        yf_ticker = f"{ticker}.TW" if market == "TW Stocks" else ticker
        data = yf.download(yf_ticker, start=start_date, end=end_date, multi_level_index=False)
        if not data.empty:
            stock_data[ticker] = data
        else:
            st.warning(f"No data found for {ticker}.")
    
    return stock_data
