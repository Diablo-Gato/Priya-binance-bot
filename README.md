#  Priya Binance Futures CLI Bot

A Python-based command-line bot to place **Market**, **Limit**, and simulated **OCO (One-Cancels-the-Other)** orders on the Binance Futures Testnet. Supports modular architecture, logging, balance validation, and secure key handling via `.env`.

---

## 🚀 Features

* ✅ Place **Market** and **Limit** orders
* ✅ Simulate **OCO** (Take-Profit + Stop) orders
* ✅ Reusable `utils` for logging, validation, and API connection
* ✅ CLI-driven with clear commands
* ✅ Secure credential handling via `.env`
* ✅ Integrated logging to `bot.log`
* ✅ Testnet-safe for practice

---

## 📁 Folder Structure

```
Priya_binance_bot/
├── main.py                  # Unified CLI entrypoint
├── .env                     # Secret keys (DO NOT COMMIT)
├── example.env              # Safe template version of .env
├── requirements.txt         # Dependencies
├── bot.log                  # Log file
├── README.md                # You're here!
│
├── src/
│   ├── market_orders.py     # Handles market orders
│   ├── limit_orders.py      # Handles limit orders
│   ├── oco_orders.py        # Simulates OCO orders
│   └── utils/
│       ├── api.py           # Connects to Binance using dotenv
│       ├── logger.py        # Custom logger
│       ├── account.py       # Balance checker
│       └── validation.py    # Quantity & price validator
```

---

## 🔧 Setup Instructions

### 1. Clone & Enter Project

```bash
git clone https://github.com/yourusername/priya_binance_bot.git
cd priya_binance_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up `.env`

```bash
cp example.env .env
```

Edit `.env` and add your Binance Testnet credentials:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret_key
BINANCE_TESTNET=True
LOG_LEVEL=DEBUG
```

---

## ▶️ Usage

All commands are run via `main.py`:

### ➔ Market Order

```bash
python main.py --type market --symbol BTCUSDT --side BUY --quantity 0.01
```

### ➔ Limit Order

```bash
python main.py --type limit --symbol BTCUSDT --side SELL --quantity 0.01 --price 70000
```

### ➔ Simulated OCO Order

```bash
python main.py --type oco --symbol BTCUSDT --side SELL --quantity 0.01 --tp 71000 --stop 68000 --sl 67900
```

---

## 🛠️ CLI Help

```bash
python main.py --help
```

Shows full list of options for order types and required arguments.

---

## 🧪 Testnet Notes

* This bot uses **Binance Futures Testnet** only.
* Get your testnet credentials from:
  [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

---

## 🛡️ Safety & Logging

* `.env` file is **ignored** by Git via `.gitignore` (✅ Safe from accidental push)
* Logs are stored in `bot.log` — useful for debugging
* All validations, balance checks, and order attempts are logged

---

## 🧠 Future Work

* ↺ OCO cancellation logic
* 📊 Advanced orders like TWAP, grid, or bracket orders
* 📊 Real-time PnL tracking

---

## 🤝 Credits

* Built by Priya as part of Binance Futures bot internship assessment
* Powered by `python-binance` and `python-dotenv`

---

## 📄 License

This project is for educational/testnet use only. Do not use on mainnet with real funds without proper safety mechanisms.

```
```
