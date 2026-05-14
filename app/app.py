import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator

st.title("📈 Smart Trading Analysis System")

# User Input
stock = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS)", "RELIANCE.NS")

# Fetch Data
data = yf.download(stock, period="6mo", interval="1d")

if not data.empty:
    st.subheader("Stock Data")
    st.line_chart(data['Close'])

    # Moving Average
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # RSI
    rsi = RSIIndicator(close=data['Close'], window=14)
    data['RSI'] = rsi.rsi()

    st.subheader("Indicators")
    st.line_chart(data[['Close', 'MA50']])

    st.subheader("RSI")
    st.line_chart(data['RSI'])

    # Signal Logic
    latest_rsi = data['RSI'].iloc[-1]
    latest_price = data['Close'].iloc[-1]
    latest_ma = data['MA50'].iloc[-1]

    st.subheader("📊 Trading Signal")

    if latest_rsi < 30 and latest_price > latest_ma:
        st.success("BUY SIGNAL 📈")
    elif latest_rsi > 70 and latest_price < latest_ma:
        st.error("SELL SIGNAL 📉")
    else:
        st.warning("HOLD / NO CLEAR SIGNAL ⚖️")

else:
    st.error("Invalid stock symbol or no data found")
