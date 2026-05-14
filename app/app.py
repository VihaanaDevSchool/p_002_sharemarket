import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Smart Trading System", layout="wide")

# 🎨 THEME VARIABLES (EDIT THESE)
PRIMARY_COLOR = "#00ADB5"
BACKGROUND_COLOR = "#0E1117"
TEXT_COLOR = "#FFFFFF"

# ------------------ CUSTOM CSS ------------------
st.markdown(f"""
<style>
body {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
}}
.stButton>button {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("https://via.placeholder.com/100", width=80)  # Replace with your logo later

with col_title:
    st.title("📈 Smart Trading Analysis System")

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Settings")

# Dropdown options
stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Wipro": "WIPRO.NS",
    "AAPL (Apple)": "AAPL",
    "TSLA (Tesla)": "TSLA",
    "GOOGL (Google)": "GOOGL",
}

crypto = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD",
}

category = st.sidebar.selectbox("Select Category", ["Stocks", "Crypto"])

if category == "Stocks":
    symbol = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
    stock = stocks[symbol]
else:
    symbol = st.sidebar.selectbox("Select Crypto", list(crypto.keys()))
    stock = crypto[symbol]

# Manual override
stock = st.sidebar.text_input("Or Enter Custom Symbol", stock)

period = st.sidebar.selectbox("Period", ["3mo", "6mo", "1y"])
interval = st.sidebar.selectbox("Interval", ["1d", "1h"])

# ------------------ FETCH DATA ------------------
data = yf.download(stock, period=period, interval=interval)

if data.empty:
    st.error("Invalid symbol or no data found")
else:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    # ------------------ INDICATORS ------------------
    data['MA50'] = data['Close'].rolling(window=50).mean()

    rsi = RSIIndicator(close=data['Close'].squeeze(), window=14)
    data['RSI'] = rsi.rsi()

    macd = MACD(close=data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_signal'] = macd.macd_signal()

    bb = BollingerBands(close=data['Close'])
    data['BB_high'] = bb.bollinger_hband()
    data['BB_low'] = bb.bollinger_lband()

    # ------------------ METRICS ------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Price", f"{data['Close'].iloc[-1]:.2f}")
    col2.metric("RSI", f"{data['RSI'].iloc[-1]:.2f}")
    col3.metric("MA50", f"{data['MA50'].iloc[-1]:.2f}")

    # ------------------ CHART ------------------
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

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # ------------------ RSI ------------------
    st.subheader("RSI")
    st.line_chart(data['RSI'])

    # ------------------ MACD ------------------
    st.subheader("MACD")
    st.line_chart(data[['MACD', 'MACD_signal']])

    # ------------------ SIGNAL ------------------
    latest_rsi = data['RSI'].iloc[-1]
    latest_price = data['Close'].iloc[-1]
    latest_ma = data['MA50'].iloc[-1]

    st.subheader("📊 Trading Signal")

    if latest_rsi < 30 and latest_price > latest_ma:
        st.success("BUY SIGNAL 📈")
    elif latest_rsi > 70 and latest_price < latest_ma:
        st.error("SELL SIGNAL 📉")
    else:
        st.warning("HOLD ⚖️")

    # ------------------ DATA ------------------
    with st.expander("Show Data"):
        st.dataframe(data.tail(50))
