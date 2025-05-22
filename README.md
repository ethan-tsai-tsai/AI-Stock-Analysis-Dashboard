# AI Stock Analysis Dashboard

A Streamlit-based web application for technical stock analysis with AI-powered recommendations. Supports multiple languages and markets.

## Features

- **Multi-market Support**: Analyze both US and Taiwan stocks
- **Technical Indicators**: 
  - Trend Indicators: SMA, EMA, Bollinger Bands, VWAP
  - Momentum Indicators: RSI, MACD, ROC, CCI
- **AI Analysis**: Get LLM-powered stock recommendations with detailed justifications
- **Multi-language UI**: English, Traditional Chinese, Simplified Chinese, Japanese
- **Interactive Charts**: Plotly-powered interactive visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/ai-stock-analysis.git
cd ai-stock-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Usage

1. Select your preferred language from the sidebar
2. Choose market type (US or Taiwan stocks)
3. Enter stock tickers (comma separated)
4. Set date range for analysis
5. Add technical indicators from the sidebar
6. Click "Generate AI Analysis" for each stock
7. View overall summary in the "Overall Summary" tab

## Supported Indicators

| Indicator | Description | Common Parameters |
|-----------|-------------|-------------------|
| SMA | Simple Moving Average | Period (default: 20) |
| EMA | Exponential Moving Average | Period (default: 20) |
| Bollinger Bands | Volatility indicator | Period (default: 20) |
| VWAP | Volume Weighted Average Price | None |
| RSI | Relative Strength Index | Period (default: 14) |
| MACD | Moving Average Convergence Divergence | Fast (12), Slow (26), Signal (9) |
| ROC | Rate of Change | Period (default: 12) |
| CCI | Commodity Channel Index | Period (default: 20) |

## License

MIT License

[中文版README](README.zh-TW.md)
