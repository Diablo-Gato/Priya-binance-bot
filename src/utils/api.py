import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

load_dotenv()

def get_binance_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("BINANCE_TESTNET", "True").lower() == "true"

    if not api_key or not api_secret:
        raise ValueError("API keys not found. Set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")

    try:
        client = Client(api_key, api_secret, testnet=use_testnet)
        client.futures_ping()
        return client
    except BinanceAPIException as e:
        raise ValueError(f"Failed to connect to Binance API. Error: {e.message}")
    except Exception as e:
        raise ValueError(f"Unexpected error during API client initialization: {e}")