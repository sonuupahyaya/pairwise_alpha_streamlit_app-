# pairwise_alpha_streamlit_app-
A high-signal crypto trading strategy that detects and exploits **delayed correlations** between a **target coin** (e.g., AVAX) and an **anchor coin** (e.g., ETH, BTC, or SOL).   This Streamlit app allows you to **analyze, backtest, and visualize** these relationships through a user-friendly web interface.


# 📈 PairWise Alpha — Lagged Correlation Crypto Strategy (Streamlit App)

A high-signal crypto trading strategy that detects and exploits **delayed correlations** between a **target coin** (e.g., AVAX) and an **anchor coin** (e.g., ETH, BTC, or SOL).  
This Streamlit app allows you to **analyze, backtest, and visualize** these relationships through a user-friendly web interface.

---

## 🚀 Features

- 🔗 Detects **lagged correlation** between coins
- ⚙️ Configurable parameters: coins, time range, lag window, thresholds
- 📊 Visualizes lag correlation and equity growth
- 💰 Simulates strategy performance via backtesting
- 🖥️ Web-based interface using **Streamlit**

---

## 📂 Project Structure




📁 pairwise_alpha_streamlit_app/
├── app.py # Streamlit application
├── requirements.txt # Required Python libraries



---

## 🧪 How the Strategy Works

1. Fetches historical price data from **Yahoo Finance**
2. Computes percentage returns and correlation between anchor & target
3. Finds the **best lag** where correlation is highest
4. Generates **BUY/SELL/HOLD** signals based on anchor coin’s earlier moves
5. Runs a **backtest** to simulate strategy performance
6. Displays final capital, return %, and charts

---

## 🛠️ How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Launch Streamlit app
streamlit run app.py


🌐 Example Use Case
If ETH pumps, and historically AVAX follows after 8 hours, the model learns this pattern and generates a BUY signal for AVAX when ETH rises.



📈 Example Output
✅ Best Lag: 6 bars (e.g., 24 hours if interval = 4h)

✅ Final Capital: $1423.50

✅ Total Return: 42.35%

📌 Requirements
Python 3.8+

Streamlit

yfinance

pandas, numpy, matplotlib

📘 License
This project is for educational and research purposes only. Not financial advice.

🙌 Acknowledgements
Data via Yahoo Finance

Built with Streamlit
