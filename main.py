import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Set LLM
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = 'deepseek/deepseek-chat-v3-0324:free'

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

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

# Butoon to fetch data
if st.sidebar.button("Fetch Data"):
    stock_data = {}
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date, multi_level_index=False)
        if not data.empty:
            stock_data[ticker] = data
        else:
            st.warning(f"No data found for {ticker}.")
    
    st.session_state["stock_data"] = stock_data
    st.success("Stock data loaded successfully for: " + ", ".join(stock_data.keys()))

# Ensure we have stock data in session state
if "stock_data" in st.session_state and st.session_state["stock_data"]:
    # buildding chat, call the LLM and getting the response
    def analyze_ticker(ticker, data):
        fig = go.Figure(data=[
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Candlestick"
            )
        ])
        # Adding technical indicators
        def add_indicator(indicator):
            nonlocal indicators_summary
            if indicator == "20-day SMA":
                sma = data['Close'].rolling(window=20).mean()
                fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA(20)'))
                indicators_summary += f"20-day SMA: {sma.values}\n"
            elif indicator == "20-Day EMA":
                ema = data['Close'].ewm(span=20).mean()
                fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA(20)'))
                indicators_summary += f"20-day EMA: {ema.values}\n"
            elif indicator == "20-Day Bollinger Bands":
                sma = data['Close'].rolling(window=20).mean()
                std = data['Close'].rolling(window=20).std()
                upper_band = sma + (std * 2)
                lower_band = sma - (std * 2)
                fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band'))
                fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band'))
                indicators_summary += f"20-day Bollinger Bands: Upper Band: {upper_band.values}, Lower Band: {lower_band.values}\n"
            elif indicator == "VWAP":
                data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
                fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'))
                indicators_summary += f"VWAP: {data['VWAP'].values}\n"
        
        indicators_summary = ""
        for ind in indicators:
            add_indicator(ind)
        fig.update_layout(xaxis_rangeslider_visible=False)

        # Update prompt asking for a detailed justification of technical analysis and recommendations
        analysis_prompt = (
            f"You are a Stock Trader specializing in Technical Analysis at a top financial institution. "
            f"Here is the summary of technical indicators for {ticker}:\n\n"f"{indicators_summary}"
            f"Provide a detailed justification of your analysis, explaining what patterns, signals, and trends you observe. "
            f"Then, based analysis results, provide a recommendation from the following options: "
            f"'Strong Buy', 'Buy', 'Weak Buy', 'Hold', 'Weak Sell', 'Sell', or 'Strong Sell'. "
            f"Return your output as a JSON object with two keys: 'action' and 'justification'."
        )

        # Call the LLM with the image part and the analysis prompt
        contents = [
            {'role': 'user', 'content': analysis_prompt}
        ]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=contents,
        )

        try:
            result_text = response.choices[0].message.content
            print(result_text)
            json_start_index = result_text.index('{')
            json_end_index = result_text.rindex('}') + 1

            if json_start_index != -1 and json_end_index > json_start_index:
                json_str = result_text[json_start_index:json_end_index]
                result = json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in the response.")
        except json.JSONDecodeError as e:
            result = {
                "action": "Error",
                "justification": f"JSON Parsing error: {e}. Raw response text: {response.choices[0].message.content}"
            }
        except ValueError as ve:
            result = {
                "action": "Error",
                "justification": f"Value Error: {ve}. Raw response text: {response.choices[0].message.content}"
            }
        except Exception as e:
            result = {
                "action": "Error",
                "justification": f"General Error: {e}. Raw response text: {response.choices[0].message.content}"
            }
        return fig, result
    
    # Create tab for overall summary, subsequent tabs per ticker
    tab_name = ["Overall Summary"] + list(st.session_state["stock_data"].keys())
    tabs = st.tabs(tab_name)

    # List to store overall results
    overall_results = []
    # Process each ticker and populate results
    for i, ticker in enumerate(st.session_state["stock_data"]):
        data = st.session_state["stock_data"][ticker]
        # Analyze ticker: get chart figure and structured output result
        fig, result = analyze_ticker(ticker, data)
        overall_results.append({"Stock": ticker, "Recommendation": result.get("action", "N/A")})
        # In each ticker-specific tab, display the chart and detailed justification
        with tabs[i + 1]:
            st.subheader(f"Analysis for {ticker}")
            st.plotly_chart(fig)
            st.write("**Detailed Justification:**")
            st.write(result.get("justification", "No justification provided."))

    # In the Overall Summary tab, display a table of all results
    with tabs[0]:
        st.subheader("Overall Structured Recommendations")
        df_summary = pd.DataFrame(overall_results)
        st.table(df_summary)
else:
    st.info("Please fetch stock data using the sidebar.")