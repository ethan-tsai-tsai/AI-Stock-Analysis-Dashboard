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

### 使用 Poetry (推薦)

1. 克隆存儲庫:
```bash
git clone https://github.com/your-repo/ai-stock-analysis.git
cd ai-stock-analysis
```

2. 安裝Poetry(如果尚未安裝):
```bash
pip install poetry
```

3. 安裝依賴項:
```bash
poetry install
```

4. 運行應用程式:
```bash
poetry run streamlit run main.py
```

### 使用 pip

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

## 配置設定

1. 複製範例檔案建立.env:
```bash
cp .env-example .env
```

2. 獲取OpenRouter API金鑰:
   - 前往 [OpenRouter網站](https://openrouter.ai/)
   - 註冊並登入帳號
   - 導航至"API Keys"部分
   - 建立新的API金鑰
   - 複製金鑰並貼到.env檔案中:
     ```
     OPENROUTER_API_KEY=your_api_key_here
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
