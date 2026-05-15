# Smart Trading Analysis System – Code Explanation

## 🔍 Overview
This project is a web-based trading dashboard built using Streamlit. It fetches real-time financial data, applies technical indicators, and generates trading signals with a simple AI assistant.

---

## ⚙️ Libraries Used

- **streamlit** – UI framework for web app
- **yfinance** – Fetch stock/crypto data
- **pandas** – Data processing
- **plotly** – Interactive charts
- **ta** – Technical indicators (RSI, MACD, Bollinger Bands)

---

## 🧱 Application Structure

### 1. Configuration
```python
st.set_page_config(...)
