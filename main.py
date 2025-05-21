import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.ui import setup_ui
from src.data_fetcher import fetch_stock_data
from src.analysis import analyze_with_llm
from src.indicators import calculate_indicators

def main():
    # Setup UI and get user inputs
    tickers, start_date, end_date, indicators = setup_ui()
    
    # Fetch stock data
    stock_data = fetch_stock_data(tickers, start_date, end_date)
    
    if stock_data:
        st.session_state["stock_data"] = stock_data
        st.success("Stock data loaded successfully for: " + ", ".join(stock_data.keys()))
        
        # Process each stock
        overall_results = []
        tab_name = ["Overall Summary"] + list(stock_data.keys())
        tabs = st.tabs(tab_name)
        
        for i, ticker in enumerate(stock_data):
            data = stock_data[ticker]
            fig, indicator_summary = calculate_indicators(data, indicators)
            result = analyze_with_llm(ticker, indicator_summary)
            
            with tabs[i + 1]:
                st.subheader(f"Analysis for {ticker}")
                st.plotly_chart(fig)
                st.write("**Detailed Justification:**")
                st.write(result.get("justification", "No justification provided."))
            
            overall_results.append({"Stock": ticker, "Recommendation": result.get("action", "N/A")})
        
        with tabs[0]:
            st.subheader("Overall Structured Recommendation")
            st.table(pd.DataFrame(overall_results))
    else:
        st.info("Please fetch stock data using the sidebar.")

if __name__ == "__main__":
    main()
