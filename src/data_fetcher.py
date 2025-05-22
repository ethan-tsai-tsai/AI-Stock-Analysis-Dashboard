import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st

def fetch_stock_data(tickers, start_date, end_date, market="US Stocks"):
    stock_data = {}
    if not tickers:  # Check if tickers list is empty
        return stock_data
        
    for ticker in tickers:
        try:
            # Add .TW suffix for Taiwan stocks
            yf_ticker = f"{ticker}.TW" if market == "TW Stocks" else ticker
            data = yf.download(
                yf_ticker,
                start=start_date,
                end=end_date,
                progress=False,
                multi_level_index=False
            )
            if not data.empty:
                # Flatten multi-index columns if present
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = ['_'.join(col).strip() for col in data.columns.values]
                stock_data[ticker] = data
            else:
                st.warning(f"No data found for {ticker}.")
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
    
    return stock_data
