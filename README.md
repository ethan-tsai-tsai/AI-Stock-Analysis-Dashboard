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

---

# AI股票分析儀表板

一個基於Streamlit的網頁應用程式，提供技術股票分析和AI驅動的投資建議，支援多種語言和市場。

## 功能特色

- **多市場支援**: 分析美股和台股
- **技術指標**: 
  - 趨勢指標: SMA, EMA, 布林通道, VWAP
  - 動量指標: RSI, MACD, ROC, CCI
- **AI分析**: 獲取基於LLM的股票建議與詳細分析
- **多語言介面**: 英文、繁體中文、簡體中文、日文
- **互動式圖表**: 使用Plotly的互動式視覺化

## 安裝說明

1. 克隆存儲庫:
```bash
git clone https://github.com/your-repo/ai-stock-analysis.git
cd ai-stock-analysis
```

2. 安裝依賴項:
```bash
pip install -r requirements.txt
```

3. 運行應用程式:
```bash
streamlit run main.py
```

## 使用說明

1. 從側邊欄選擇語言
2. 選擇市場類型(美股或台股)
3. 輸入股票代碼(多個代碼用逗號分隔)
4. 設定分析日期範圍
5. 從側邊欄添加技術指標
6. 點擊"Generate AI Analysis"獲取每支股票分析
7. 在"Overall Summary"標籤查看整體建議

## 支援指標

| 指標 | 說明 | 常用參數 |
|------|------|----------|
| SMA | 簡單移動平均線 | 週期(預設:20) |
| EMA | 指數移動平均線 | 週期(預設:20) |
| 布林通道 | 波動率指標 | 週期(預設:20) |
| VWAP | 成交量加權平均價 | 無 |
| RSI | 相對強弱指數 | 週期(預設:14) |
| MACD | 指數平滑異同移動平均線 | 快線(12),慢線(26),信號線(9) |
| ROC | 變動率指標 | 週期(預設:12) |
| CCI | 商品通道指數 | 週期(預設:20) |

## 授權資訊

MIT授權
