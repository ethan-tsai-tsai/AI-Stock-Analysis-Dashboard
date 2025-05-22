import streamlit as st
from datetime import datetime, timedelta
import uuid

def setup_ui():
    # Set Streamlit page configuration
    st.set_page_config(layout='wide')
    st.title('Technical Stock Analysis Dashboard')
    st.sidebar.header("Configuration")

    # Language selection in sidebar with icon hover
    with st.sidebar:
        with st.popover("🌐 Language", help="Select language"):
            language = st.radio(
                "Language",
                options=["English", "繁體中文", "简体中文", "日本語"],
                index=0,
                label_visibility="collapsed"
            )

    # Market type selection
    market = st.sidebar.selectbox(
        "Market Type",
        options=["US Stocks", "TW Stocks"],
        index=0
    )

    # Input for stock tickers
    ticker_label = "Enter stock tickers (comma-separated)" + (" e.g. 2330, 2317" if market == "TW Stocks" else " e.g. AAPL, MSFT")
    tickers_input = st.sidebar.text_input(ticker_label, "AAPL, MSFT" if market == "US Stocks" else "2330, 2317")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',') if ticker.strip()]

    # Set the data range: start date and end date
    end_date_default = datetime.now()
    start_date_default = end_date_default - timedelta(days=365)
    start_date = st.sidebar.date_input('Start date', start_date_default)
    end_date = st.sidebar.date_input('End date', end_date_default)

    # Technical indicators selection with add button
    st.sidebar.subheader('Technical Indicators')
    
    # Initialize session state for indicators
    if 'indicators' not in st.session_state:
        st.session_state.indicators = []
        st.session_state.indicator_params = {}
    
    # Add Indicator button at the bottom
    with st.sidebar:
        st.markdown("---")
        with st.popover("+ Add Indicator", help="Click to add technical indicators"):
            indicator_type = st.selectbox(
                "Select Indicator",
                options=["SMA", "EMA", "Bollinger Bands", "VWAP", "RSI", "MACD", "ROC", "CCI"],
                key="indicator_select"
            )
            
            # Get parameters based on selected indicator
            params = {}
            if indicator_type == "SMA":
                period = st.number_input("Period", min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "EMA":
                period = st.number_input("Period", min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "Bollinger Bands":
                period = st.number_input("Period", min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "RSI":
                period = st.number_input("Period", min_value=1, value=14)
                params["period"] = max(1, period)
            elif indicator_type == "MACD":
                fast = st.number_input("Fast Period", min_value=1, value=12)
                slow = st.number_input("Slow Period", min_value=1, value=26)
                signal = st.number_input("Signal Period", min_value=1, value=9)
                params["fast"] = max(1, fast)
                params["slow"] = max(1, slow)
                params["signal"] = max(1, signal)
            elif indicator_type == "ROC":
                period = st.number_input("Period", min_value=1, value=12)
                params["period"] = max(1, period)
            elif indicator_type == "CCI":
                period = st.number_input("Period", min_value=1, value=20)
                params["period"] = max(1, period)
            
            if st.button("Add Indicator"):
                indicator_id = str(uuid.uuid4())
                display_name = f"{indicator_type}({params.get('period', params.get('fast', ''))})"
                st.session_state.indicators.append({
                    "id": indicator_id,
                    "type": indicator_type,
                    "params": params,
                    "display_name": display_name
                })

    # Display and manage selected indicators
    if st.session_state.indicators:
        st.sidebar.write("**Selected Indicators:**")
        for idx, indicator in enumerate(st.session_state.indicators[:]):  # Make a copy for iteration
            with st.sidebar.expander(indicator["display_name"]):
                # Display current parameters
                st.write("Parameters:")
                
                # Edit parameters
                new_params = {}
                if indicator["type"] == "SMA":
                    new_period = st.number_input("Period", 
                        min_value=1, 
                        value=indicator["params"].get("period", 20),
                        key=f"sma_period_{indicator['id']}")
                    new_params["period"] = new_period
                # Add similar edit controls for other indicator types...
                
                if st.button("Update", key=f"update_{indicator['id']}"):
                    # Update parameters and display name
                    indicator["params"] = new_params
                    indicator["display_name"] = f"{indicator['type']}({new_params.get('period', new_params.get('fast', ''))})"
                    st.rerun()
                
                if st.button("Remove", key=f"remove_{indicator['id']}"):
                    st.session_state.indicators.pop(idx)
                    st.rerun()

    # Prepare output for other modules
    indicators_list = [ind["type"] for ind in st.session_state.indicators]
    indicator_params = st.session_state.indicator_params

    return tickers, start_date, end_date, indicators_list, indicator_params, language, market
