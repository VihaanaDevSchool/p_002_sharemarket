import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

st.set_page_config(page_title="Smart Trading System", layout="wide")

st.title("📈 Smart Trading Analysis System")

# Sidebar
st.sidebar.header("Settings")
stock = st.sidebar.text_input("Stock Symbol", "RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["3mo", "6mo", "1y"])
interval = st.sidebar.selectbox("Interval", ["1d", "1h"])

# Fetch Data
data = yf.download(stock, period=period, interval=interval)

if data.empty:
    st.error("Invalid stock symbol or no data found")
else:
    # Fix multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    # Indicators
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # RSI
    rsi = RSIIndicator(close=data['Close'].squeeze(), window=14)
    data['RSI'] = rsi.rsi()

    # MACD
    macd = MACD(close=data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_signal'] = macd.macd_signal()

    # Bollinger Bands
    bb = BollingerBands(close=data['Close'])
    data['BB_high'] = bb.bollinger_hband()
    data['BB_low'] = bb.bollinger_lband()

    # ---- UI Layout ----
    col1, col2, col3 = st.columns(3)

    col1.metric("Latest Price", f"{data['Close'].iloc[-1]:.2f}")
    col2.metric("RSI", f"{data['RSI'].iloc[-1]:.2f}")
    col3.metric("MA50", f"{data['MA50'].iloc[-1]:.2f}")

    # ---- Candlestick Chart ----
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    ))

    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA50'))

    fig.add_trace(go.Scatter(x=data.index, y=data['BB_high'], name='BB High', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_low'], name='BB Low', line=dict(dash='dot')))

    st.plotly_chart(fig, use_container_width=True)

    # ---- RSI Chart ----
    st.subheader("RSI Indicator")
    st.line_chart(data['RSI'])

    # ---- MACD Chart ----
    st.subheader("MACD Indicator")
    st.line_chart(data[['MACD', 'MACD_signal']])

    # ---- Signal Logic ----
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

    # ---- Data Table ----
    with st.expander("Show Raw Data"):
        st.dataframe(data.tail(50))
