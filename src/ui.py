import streamlit as st
from datetime import datetime, timedelta
import uuid

# Translation dictionary
TRANSLATIONS = {
    "English": {
        "title": "Technical Stock Analysis Dashboard",
        "config": "Configuration",
        "language": "Language",
        "market": "Market Type",
        "ticker_input": "Enter stock tickers (comma-separated)",
        "start_date": "Start date",
        "end_date": "End date",
        "indicators": "Technical Indicators",
        "add_indicator": "+ Add Indicator",
        "select_indicator": "Select Indicator",
        "period": "Period",
        "fast_period": "Fast Period",
        "slow_period": "Slow Period",
        "signal_period": "Signal Period",
        "update": "Update",
        "remove": "Remove",
        "selected_indicators": "Selected Indicators:",
        "parameters": "Parameters:"
    },
    "繁體中文": {
        "title": "股票技術分析儀表板",
        "config": "設定",
        "language": "語言",
        "market": "市場類型",
        "ticker_input": "輸入股票代碼 (以逗號分隔)",
        "start_date": "開始日期",
        "end_date": "結束日期",
        "indicators": "技術指標",
        "add_indicator": "+ 新增指標",
        "select_indicator": "選擇指標",
        "period": "週期",
        "fast_period": "快速週期",
        "slow_period": "慢速週期",
        "signal_period": "信號週期",
        "update": "更新",
        "remove": "移除",
        "selected_indicators": "已選指標:",
        "parameters": "參數:"
    },
    "简体中文": {
        "title": "股票技术分析仪表板",
        "config": "设置",
        "language": "语言",
        "market": "市场类型",
        "ticker_input": "输入股票代码 (以逗号分隔)",
        "start_date": "开始日期",
        "end_date": "结束日期",
        "indicators": "技术指标",
        "add_indicator": "+ 添加指标",
        "select_indicator": "选择指标",
        "period": "周期",
        "fast_period": "快速周期",
        "slow_period": "慢速周期",
        "signal_period": "信号周期",
        "update": "更新",
        "remove": "移除",
        "selected_indicators": "已选指标:",
        "parameters": "参数:"
    },
    "日本語": {
        "title": "株式テクニカル分析ダッシュボード",
        "config": "設定",
        "language": "言語",
        "market": "市場タイプ",
        "ticker_input": "株式コードを入力 (カンマ区切り)",
        "start_date": "開始日",
        "end_date": "終了日",
        "indicators": "テクニカル指標",
        "add_indicator": "+ 指標を追加",
        "select_indicator": "指標を選択",
        "period": "期間",
        "fast_period": "短期間",
        "slow_period": "長期間",
        "signal_period": "シグナル期間",
        "update": "更新",
        "remove": "削除",
        "selected_indicators": "選択された指標:",
        "parameters": "パラメータ:"
    }
}

def setup_ui():
    # Set Streamlit page configuration
    st.set_page_config(layout='wide')
    
    # Language selection in sidebar with icon hover
    with st.sidebar:
        with st.popover("🌐 Language", help="Select language"):
            language = st.radio(
                TRANSLATIONS["English"]["language"],
                options=["English", "繁體中文", "简体中文", "日本語"],
                index=0,
                label_visibility="collapsed"
            )
    
    # Get translations for selected language
    t = TRANSLATIONS[language]
    
    st.title(t["title"])
    st.sidebar.header(t["config"])

    # Market type selection
    market = st.sidebar.selectbox(
        t["market"],
        options=["US Stocks", "TW Stocks"],
        index=0
    )

    # Input for stock tickers
    ticker_label = t["ticker_input"] + (" e.g. 2330, 2317" if market == "TW Stocks" else " e.g. AAPL, MSFT")
    tickers_input = st.sidebar.text_input(ticker_label, "AAPL, MSFT" if market == "US Stocks" else "2330, 2317")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',') if ticker.strip()]

    # Set the data range: start date and end date
    end_date_default = datetime.now()
    start_date_default = end_date_default - timedelta(days=365)
    start_date = st.sidebar.date_input(t["start_date"], start_date_default)
    end_date = st.sidebar.date_input(t["end_date"], end_date_default)

    # Technical indicators selection with add button
    st.sidebar.subheader(t["indicators"])
    
    # Initialize session state for indicators
    if 'indicators' not in st.session_state:
        st.session_state.indicators = []
        st.session_state.indicator_params = {}
    
    # Add Indicator button at the bottom
    with st.sidebar:
        st.markdown("---")
        with st.popover(t["add_indicator"], help="Click to add technical indicators"):
            indicator_type = st.selectbox(
                t["select_indicator"],
                options=["SMA", "EMA", "Bollinger Bands", "VWAP", "RSI", "MACD", "ROC", "CCI"],
                key="indicator_select"
            )
            
            # Get parameters based on selected indicator
            params = {}
            if indicator_type == "SMA":
                period = st.number_input(t["period"], min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "EMA":
                period = st.number_input(t["period"], min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "Bollinger Bands":
                period = st.number_input(t["period"], min_value=1, value=20)
                params["period"] = max(1, period)
            elif indicator_type == "RSI":
                period = st.number_input(t["period"], min_value=1, value=14)
                params["period"] = max(1, period)
            elif indicator_type == "MACD":
                fast = st.number_input(t["fast_period"], min_value=1, value=12)
                slow = st.number_input(t["slow_period"], min_value=1, value=26)
                signal = st.number_input(t["signal_period"], min_value=1, value=9)
                params["fast"] = max(1, fast)
                params["slow"] = max(1, slow)
                params["signal"] = max(1, signal)
            elif indicator_type == "ROC":
                period = st.number_input(t["period"], min_value=1, value=12)
                params["period"] = max(1, period)
            elif indicator_type == "CCI":
                period = st.number_input(t["period"], min_value=1, value=20)
                params["period"] = max(1, period)
            
            if st.button(t["add_indicator"]):
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
        st.sidebar.write(f"**{t['selected_indicators']}**")
        for idx, indicator in enumerate(st.session_state.indicators[:]):  # Make a copy for iteration
            with st.sidebar.expander(indicator["display_name"]):
                # Display current parameters
                st.write(f"{t['parameters']}")
                
                # Edit parameters
                new_params = {}
                if indicator["type"] == "SMA":
                    new_period = st.number_input(t["period"], 
                        min_value=1, 
                        value=indicator["params"].get("period", 20),
                        key=f"sma_period_{indicator['id']}")
                    new_params["period"] = new_period
                # Add similar edit controls for other indicator types...
                
                if st.button(t["update"], key=f"update_{indicator['id']}"):
                    # Update parameters and display name
                    indicator["params"] = new_params
                    indicator["display_name"] = f"{indicator['type']}({new_params.get('period', new_params.get('fast', ''))})"
                    st.rerun()
                
                if st.button(t["remove"], key=f"remove_{indicator['id']}"):
                    st.session_state.indicators.pop(idx)
                    st.rerun()

    # Prepare output for other modules
    indicators_list = [ind["type"] for ind in st.session_state.indicators]
    indicator_params = st.session_state.indicator_params

    return tickers, start_date, end_date, indicators_list, indicator_params, language, market
