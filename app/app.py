import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Smart Trading System",
    layout="wide",
    page_icon="./img/logo.webp"  # ✅ FAVICON ADDED
)

# 🎨 YOUR COLORS
COLOR1 = "#b512fa"
COLOR2 = "#6f3afd"
COLOR3 = "#09a8ec"

# ------------------ CUSTOM CSS ------------------
st.markdown(f"""
<style>
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLOR1}, {COLOR2}, {COLOR3});
}}
body {{
    color: white;
}}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("./img/logo.webp", width=80)

with col_title:
    st.title("🚀 Smart Trading Dashboard")

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Settings")

stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "AAPL": "AAPL",
    "TSLA": "TSLA",
    "GOOGL": "GOOGL",
}

crypto = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD",
}

category = st.sidebar.selectbox("Category", ["Stocks", "Crypto"])

if category == "Stocks":
    symbol = st.sidebar.selectbox("Stock", list(stocks.keys()))
    stock = stocks[symbol]
else:
    symbol = st.sidebar.selectbox("Crypto", list(crypto.keys()))
    stock = crypto[symbol]

stock = st.sidebar.text_input("Custom Symbol", stock)

period = st.sidebar.selectbox("Period", ["3mo", "6mo", "1y"])
interval = st.sidebar.selectbox("Interval", ["1d", "1h"])

# ------------------ FETCH DATA ------------------
data = yf.download(stock, period=period, interval=interval)

if data.empty:
    st.error("Invalid symbol")
else:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    # ------------------ TOP MOVERS (NOW AT TOP) ------------------
    st.subheader("🔥 Market Movers")

    demo_symbols = ["RELIANCE.NS", "TCS.NS", "AAPL", "BTC-USD"]
    cols = st.columns(len(demo_symbols))

    for i, sym in enumerate(demo_symbols):
        d = yf.download(sym, period="5d", interval="1d")

        if not d.empty and 'Close' in d:
            start_price = float(d['Close'].iloc[0])
            end_price = float(d['Close'].iloc[-1])
            change = end_price - start_price

            if change > 0:
                cols[i].success(f"{sym} ↑")
            else:
                cols[i].error(f"{sym} ↓")

    # ------------------ INDICATORS ------------------
    data['MA50'] = data['Close'].rolling(50).mean()

    rsi = RSIIndicator(close=data['Close'].squeeze())
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

    # ------------------ SIGNAL (NOW BELOW MOVERS) ------------------
    latest_rsi = data['RSI'].iloc[-1]
    latest_price = data['Close'].iloc[-1]
    latest_ma = data['MA50'].iloc[-1]

    st.subheader("✨ Trading Signal")

    if latest_rsi < 30 and latest_price > latest_ma:
        st.success("BUY 📈")
        sentiment = 80
    elif latest_rsi > 70 and latest_price < latest_ma:
        st.error("SELL 📉")
        sentiment = 20
    else:
        st.warning("HOLD ⚖️")
        sentiment = 50

    # ------------------ MARKET SENTIMENT ------------------
    st.subheader("🏮 Market Sentiment")
    st.progress(sentiment / 100)

    # ------------------ CANDLESTICK ------------------
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA50'],
        name='MA50',
        line=dict(color="#00ffcc")
    ))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, width='stretch')

    # ------------------ RSI ------------------
    st.subheader("💪🏻 RSI (Momentum)")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(
        x=data.index,
        y=data['RSI'],
        line=dict(color="yellow", width=2)
    ))
    st.plotly_chart(fig_rsi, width='stretch')

    # ------------------ MACD ------------------
    st.subheader("🪂 MACD (Trend)")
    fig_macd = go.Figure()

    fig_macd.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD'],
        name="MACD",
        line=dict(color="pink")
    ))

    fig_macd.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD_signal'],
        name="Signal",
        line=dict(color="cyan")
    ))

    st.plotly_chart(fig_macd, width='stretch')

    # ------------------ DATA ------------------
    with st.expander("Show Data"):
        st.dataframe(data.tail(30))

        # ------------------ AI ASSISTANT ------------------

# Generate AI message
if latest_rsi < 30 and latest_price > latest_ma:
    ai_msg = "🤖 Strong BUY signal detected. Momentum is rising."
elif latest_rsi > 70 and latest_price < latest_ma:
    ai_msg = "🤖 Market looks overbought. Consider SELLING."
elif latest_price > latest_ma:
    ai_msg = "🤖 Uptrend forming. Watch for breakout."
elif latest_price < latest_ma:
    ai_msg = "🤖 Downtrend detected. Be cautious."
else:
    ai_msg = "🤖 Market is sideways. Wait for clear signal."

# Floating UI
st.markdown(f"""
<style>
#ai-box {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 260px;
    background: linear-gradient(135deg, #6f3afd, #09a8ec);
    padding: 15px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
    z-index: 9999;
    font-size: 14px;
}}
#ai-box img {{
    width: 40px;
    margin-bottom: 8px;
}}
</style>

<div id="ai-box">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png">
    <b>AI Assistant</b><br>
    {ai_msg}
</div>
""", unsafe_allow_html=True)
