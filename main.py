import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.ui import setup_ui
from src.data_fetcher import fetch_stock_data
from src.analysis import analyze_with_llm
from src.indicators import calculate_indicators

def main():
    # Setup UI and get user inputs
    tickers, start_date, end_date, indicators_list, indicator_params, language, market = setup_ui()
    
    # Fetch stock data
    stock_data = fetch_stock_data(tickers, start_date, end_date, market)
    
    if stock_data:
        st.session_state["stock_data"] = stock_data
        st.success("Stock data loaded successfully for: " + ", ".join(stock_data.keys()))
        
        # Process each stock
        overall_results = []
        tab_name = list(stock_data.keys()) + ["Overall Summary"]
        tabs = st.tabs(tab_name)
        
        for i, ticker in enumerate(stock_data):
            data = stock_data[ticker]
            fig, indicator_summary = calculate_indicators(data, st.session_state.indicators, indicator_params)
            
            with tabs[i]:  # First tabs are for stock analysis
                st.subheader(f"Analysis for {ticker}")
                st.plotly_chart(fig)
                
                if st.button(f"Generate AI Analysis for {ticker}", key=f"analyze_{ticker}"):
                    with st.spinner(f"Generating {language} analysis for {ticker}..."):
                        result = analyze_with_llm(ticker, indicator_summary, language)
                        st.session_state[f"analysis_{ticker}"] = result
                
                if f"analysis_{ticker}" in st.session_state:
                    result = st.session_state[f"analysis_{ticker}"]
                    justification = result.get("justification", "No justification provided.")
                    st.write("**Detailed Justification:**")
                    st.write_stream((c for c in justification))
            
            if f"analysis_{ticker}" in st.session_state:
                result = st.session_state[f"analysis_{ticker}"]
                overall_results.append({"Stock": ticker, "Recommendation": result.get("action", "N/A")})
            else:
                overall_results.append({"Stock": ticker, "Recommendation": "Not analyzed"})
        
        with tabs[-1]:  # Last tab is Overall Summary
            st.subheader("Overall Structured Recommendation")
            st.table(pd.DataFrame(overall_results))
    else:
        st.info("Please fetch stock data using the sidebar.")

if __name__ == "__main__":
    main()
