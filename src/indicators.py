import plotly.graph_objects as go
import pandas as pd
import json

def calculate_indicators(data, indicators):
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
    
    indicators_summary = {}
    
    def add_indicator(indicator):
        nonlocal indicators_summary
        if indicator == "20-day SMA":
            sma = data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA(20)'))
            indicators_summary["20-day_SMA"] = sma.values.tolist()
        elif indicator == "20-Day EMA":
            ema = data['Close'].ewm(span=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA(20)'))
            indicators_summary["20-day_EMA"] = ema.values.tolist()
        elif indicator == "20-Day Bollinger Bands":
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            upper_band = sma + (std * 2)
            lower_band = sma - (std * 2)
            fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band'))
            fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band'))
            indicators_summary["20-day_Bollinger_Bands"] = {
                "upper_band": upper_band.values.tolist(),
                "lower_band": lower_band.values.tolist()
            }
        elif indicator == "VWAP":
            data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
            fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'))
            indicators_summary["VWAP"] = data['VWAP'].values.tolist()
    
    for ind in indicators:
        add_indicator(ind)
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig, json.dumps(indicators_summary)
