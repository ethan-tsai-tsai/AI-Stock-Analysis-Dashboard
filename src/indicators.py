import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json

def calculate_indicators(data, indicators, indicator_params):
    # Clear any existing figures
    go.Figure().data = []
    go.Figure().layout = {}
    
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3]
    )
    
    # Add candlestick to main chart (row 1)
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlestick"
        ),
        row=1, col=1
    )
    
    indicators_summary = {}

    def calculate_rsi(data, window):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(data, fast, slow, signal):
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        return macd, signal_line

    def calculate_roc(data, window):
        return ((data['Close'] - data['Close'].shift(window)) / data['Close'].shift(window)) * 100

    def calculate_cci(data, window):
        tp = (data['High'] + data['Low'] + data['Close']) / 3
        sma = tp.rolling(window=window).mean()
        mad = tp.rolling(window=window).apply(lambda x: abs(x - x.mean()).mean())
        return (tp - sma) / (0.015 * mad)
    
    def add_indicator(indicator):
        nonlocal indicators_summary
        if isinstance(indicator, dict):  # New format with ID
            indicator_type = indicator["type"]
            params = indicator["params"]
        else:  # Old format (string)
            indicator_type = indicator
            params = indicator_params.get(indicator_type, {})
        
        if indicator_type == "SMA":
            period = int(params.get("period", 20))
            sma = data['Close'].rolling(window=max(1, period)).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name=f'SMA({period})'), row=1, col=1)
            indicators_summary[f"SMA_{period}"] = sma.values.tolist()
        elif indicator_type == "EMA":
            period = int(params.get("period", 20))
            ema = data['Close'].ewm(span=max(1, period)).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name=f'EMA({period})'), row=1, col=1)
            indicators_summary[f"EMA_{period}"] = ema.values.tolist()
        elif indicator == "Bollinger Bands":
            period = indicator_params["Bollinger_Bands"]
            sma = data['Close'].rolling(window=period).mean()
            std = data['Close'].rolling(window=period).std()
            upper_band = sma + (std * 2)
            lower_band = sma - (std * 2)
            fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name=f'Upper Band({period})'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name=f'Lower Band({period})'), row=1, col=1)
            indicators_summary[f"Bollinger_Bands_{period}"] = {
                "upper_band": upper_band.values.tolist(),
                "lower_band": lower_band.values.tolist()
            }
        elif indicator == "VWAP":
            data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
            fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'), row=1, col=1)
            indicators_summary["VWAP"] = data['VWAP'].values.tolist()
        elif indicator == "RSI":
            params = indicator_params.get(indicator, {"RSI": 14})  # Get the params dict for this indicator
            period = int(params.get("RSI", 14))  # Get period from params dict
            rsi = calculate_rsi(data, max(1, period))
            fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name=f'RSI({period})'), row=2, col=1)
            indicators_summary[f"RSI_{period}"] = rsi.values.tolist()
        elif indicator == "MACD":
            fast = int(indicator_params["MACD_Fast"])
            slow = int(indicator_params["MACD_Slow"])
            signal = int(indicator_params["MACD_Signal"])
            macd, signal_line = calculate_macd(data, fast, slow, signal)
            fig.add_trace(go.Scatter(x=data.index, y=macd, mode='lines', name=f'MACD({fast},{slow})'), row=2, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=signal_line, mode='lines', name=f'Signal({signal})'), row=2, col=1)
            indicators_summary["MACD"] = {
                "MACD": macd.values.tolist(),
                "Signal": signal_line.values.tolist(),
                "params": {"fast": fast, "slow": slow, "signal": signal}
            }
        elif indicator == "ROC":
            period = int(indicator_params["ROC"])
            roc = calculate_roc(data, max(1, period))
            fig.add_trace(go.Scatter(x=data.index, y=roc, mode='lines', name=f'ROC({period})'), row=2, col=1)
            indicators_summary[f"ROC_{period}"] = roc.values.tolist()
        elif indicator == "CCI":
            period = indicator_params["CCI"]
            cci = calculate_cci(data, period)
            fig.add_trace(go.Scatter(x=data.index, y=cci, mode='lines', name=f'CCI({period})'), row=2, col=1)
            indicators_summary[f"CCI_{period}"] = cci.values.tolist()
    
    for ind in indicators:
        add_indicator(ind)
    
    # Update layout
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=True,
        legend=dict(orientation="h", y=1.1)
    )
    fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
    return fig, json.dumps(indicators_summary)
