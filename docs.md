# Smart Trading Analysis System – Code Explanation

## Overview
This project is a web-based trading dashboard built using Streamlit. It fetches real-time financial data, applies technical indicators, and generates trading signals with a simple AI assistant.

## Libraries Used
- streamlit – UI framework
- yfinance – Fetch stock/crypto data
- pandas – Data processing
- plotly – Charts
- ta – Technical indicators

## Application Flow

### 1. Configuration
Sets page title, layout, and favicon.

### 2. Custom Styling
- Gradient sidebar
- Dark UI theme

### 3. Header
Displays logo and dashboard title.

### 4. Sidebar Inputs
User selects:
- Stock or Crypto
- Symbol
- Time period
- Interval

### 5. Data Fetching
Fetches real-time data using yfinance.

### 6. Market Movers
- Shows top symbols
- Green = price increased
- Red = price decreased

### 7. Indicators
- MA50 (Moving Average)
- RSI (Momentum)
- MACD (Trend)
- Bollinger Bands (Volatility)

### 8. Metrics
Displays:
- Current price
- RSI value
- MA50 value

### 9. Trading Signal Logic
- BUY → RSI < 30 and price > MA
- SELL → RSI > 70 and price < MA
- HOLD → otherwise

### 10. Market Sentiment
Progress bar showing signal strength.

### 11. Charts
- Candlestick chart
- RSI chart
- MACD chart

### 12. AI Assistant
Floating box showing suggestions based on indicators.

### 13. Data Table
Expandable section showing recent data.

## Features
- Real-time analysis
- Stock + Crypto support
- AI suggestions
- Interactive charts

## Limitations
- No real AI (rule-based)
- Depends on API
- No login system

## Future Scope
- ML predictions
- Alerts
- Portfolio tracking

## Conclusion
Helps users analyze market trends and make decisions using technical indicators.
