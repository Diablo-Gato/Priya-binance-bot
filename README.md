# Binance Futures Trading Bot

A command-line trading bot for **Binance Futures** that supports placing:
- ✅ Market Orders
- ✅ Limit Orders
- ✅ Simulated OCO (One-Cancels-the-Other) Orders
- ✅ TWAP (Time-Weighted Average Price) Orders
- ✅ Grid Orders

This bot is designed for testing, learning, and small-scale automation on Binance Futures Testnet.

---

## 🚀 Features

- Supports **Market**, **Limit**, **Simulated OCO**, **TWAP**, and **Grid** order types
- Easy CLI interface using `argparse`
- Built-in **validation**, **balance check**, and **error logging**
- Modular and extensible code structure
- Logger with `bot.log` output

---

## 📁 Folder Structure

```
Priya_binance_bot/
├── main.py
├── .gitignore
├── README.md
├── requirements.txt
├── example.env
│
└── src/
    ├── market_orders.py
    ├── limit_orders.py
    ├── oco_orders.py
    └── advanced/
    │   ├── twap.py
    │   └── grid.py
    │
    └── utils/
        ├── api.py
        ├── logger.py
        ├── account.py
        └── validation.py
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
$ git clone https://github.com/Diablo-Gato/Priya-binance-bot.git
$ cd Priya_binance_bot

# Create virtual environment
$ python -m venv venv
$ .\venv\Scripts\activate     # On Windows

# Install dependencies
$ pip install -r requirements.txt

# Copy and configure your environment variables
$ cp example.env .env
```

> Note: Do NOT commit your `.env` file to GitHub.

---

## ✅ CLI Usage Examples

### Market Order
```bash
python main.py --type market --symbol BTCUSDT --side BUY --quantity 0.01
```

### Limit Order
```bash
python main.py --type limit --symbol BTCUSDT --side SELL --quantity 0.01 --price 69000
```

### Simulated OCO Order
```bash
python main.py --type oco --symbol BTCUSDT --side SELL --quantity 0.01 --tp 71000 --stop 68000 --sl 67900
```

### TWAP Order
```bash
python -m src.advanced.twap --symbol BTCUSDT --side BUY --total_quantity 0.03 --num_slices 3 --interval 5 --type MARKET
```

### Grid Orders
```bash
python -m src.advanced.grid --symbol BTCUSDT --side BUY --total_quantity 0.05 --lower_price 67000 --upper_price 69000 --grid_count 5
```

---

## 🧠 Testnet Setup

To get API keys:
- Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
- Go to the API Management section to generate keys

Add them to your `.env` like so:
```
BINANCE_API_KEY=your_testnet_key_here
BINANCE_API_SECRET=your_testnet_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

---

## 📜 Logging

All bot activity is logged to `bot.log`.

---

## 🧪 Future Work

- Implement real-time WebSocket-based OCO cancellation logic
- Add daily PnL tracking module
- Extend TWAP with dynamic price adjustment (VWAP-based)

---

## 🛡️ Disclaimer

This bot is for educational and testing purposes on Binance **Futures Testnet** only. Use at your own risk. Always review and test any trading logic before deploying to real funds.

---

## 👩‍💻 Author

Created by [Diablo-Gato](https://github.com/Diablo-Gato).
