# app.py — Streamlit version of PairWise Alpha Strategy

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 PairWise Alpha", layout="centered")
st.title("🔗 PairWise Alpha — Lagged Crypto Strategy")

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Strategy Settings")
target_symbol = st.sidebar.text_input("Target Coin (e.g., AVAX-USD)", "AVAX-USD")
anchor_symbol = st.sidebar.text_input("Anchor Coin (e.g., ETH-USD)", "ETH-USD")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))
interval = st.sidebar.selectbox("Interval", ["1h", "4h", "1d"], index=1)
max_lag = st.sidebar.slider("Max Lag (bars)", 1, 48, 24)
corr_threshold = st.sidebar.slider("Min Correlation", 0.0, 1.0, 0.3, 0.05)
price_threshold = st.sidebar.slider("Return Threshold (%)", 0.1, 5.0, 1.0, 0.1) / 100

# --- Fetch Data ---
@st.cache_data(show_spinner=False)
def fetch(symbol):
    return yf.download(symbol, start=start_date, end=end_date, interval=interval)["Close"].dropna()

try:
    anchor = fetch(anchor_symbol)
    target = fetch(target_symbol)
    combined = pd.DataFrame({"anchor": anchor, "target": target}).dropna()

    anchor_ret = combined["anchor"].pct_change().dropna()
    target_ret = combined["target"].pct_change().dropna()

    # --- Lagged Correlation ---
    def compute_lagged_corr(ar, tr, max_lag):
        return pd.Series({lag: ar.shift(lag).corr(tr) for lag in range(1, max_lag + 1)})

    lagged_corr = compute_lagged_corr(anchor_ret, target_ret, max_lag)
    best_lag = lagged_corr.idxmax() if lagged_corr.max() > corr_threshold else None

    st.subheader("📊 Lag Analysis")
    st.line_chart(lagged_corr)
    if best_lag:
        st.success(f"✅ Best Lag = {best_lag} bars (Interval = {interval})")
    else:
        st.warning("❌ No significant lag correlation found above threshold.")

    # --- Generate Signal ---
    def generate_signal(ar, lag, thresh):
        signal = []
        for i in range(len(ar)):
            if i < lag:
                signal.append("HOLD")
            else:
                r = ar.iloc[i - lag]
                if r > thresh:
                    signal.append("BUY")
                elif r < -thresh:
                    signal.append("SELL")
                else:
                    signal.append("HOLD")
        return pd.Series(signal, index=ar.index)

    signals = generate_signal(anchor_ret, best_lag, price_threshold) if best_lag else pd.Series("HOLD", index=anchor_ret.index)

    # --- Backtest ---
    def backtest(signals, prices):
        pos, cap, hist = 0, 1000, []
        for i in range(1, len(signals)):
            p = prices.iloc[i]
            if signals.iloc[i] == "BUY" and pos == 0:
                pos = cap / p
                cap = 0
            elif signals.iloc[i] == "SELL" and pos > 0:
                cap = pos * p
                pos = 0
            val = cap + pos * p
            hist.append(val)
        return pd.Series(hist, index=prices.index[-len(hist):])

    result = backtest(signals, combined['target'])

    # --- Output ---
    st.subheader("📈 Strategy Backtest")
    st.line_chart(result)
    st.metric("Final Capital", f"${result.iloc[-1]:.2f}")
    st.metric("Total Return", f"{(result.iloc[-1] - 1000)/1000*100:.2f}%")

except Exception as e:
    st.error(f"❌ Error: {e}")
