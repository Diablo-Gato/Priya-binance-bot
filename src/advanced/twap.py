# src/advanced/twap.py

import time
import argparse
from decimal import Decimal
from binance.exceptions import BinanceAPIException
from src.utils.api import get_binance_client
from src.utils.logger import setup_logger
from src.utils.account import has_sufficient_balance
from src.utils.validation import validate_order_params

logger = setup_logger()
client = get_binance_client()

def place_twap_orders(symbol: str, side: str, total_quantity: float, num_slices: int, interval: int, order_type: str = "MARKET"):
    """
    Places TWAP (Time-Weighted Average Price) orders by splitting total_quantity
    into num_slices and placing orders at fixed intervals.

    Args:
        symbol (str): Trading pair (e.g., BTCUSDT)
        side (str): BUY or SELL
        total_quantity (float): Total quantity to buy/sell
        num_slices (int): Number of order slices
        interval (int): Interval in seconds between each order
        order_type (str): Order type - "MARKET" or "LIMIT"
    """
    try:
        slice_qty = round(total_quantity / num_slices, 6)

        logger.info(f"Starting TWAP: {num_slices} slices of {slice_qty} {symbol} every {interval}s.")


        for i in range(num_slices):
            logger.debug(f"Placing slice {i+1}/{num_slices}")

            validate_order_params(client, symbol, slice_qty)

            # Use current mark price for estimating cost
            price = float(client.futures_mark_price(symbol=symbol)["markPrice"])
            if not has_sufficient_balance(client, symbol, side, slice_qty, price):
                raise ValueError("Insufficient balance for TWAP slice.")

            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=slice_qty,
                timeInForce='GTC' if order_type == 'LIMIT' else None
            )

            logger.info(f"TWAP Order {i+1}: ID {order['orderId']}, Qty: {slice_qty}, Status: {order['status']}")
            print(f"✅ Order {i+1}/{num_slices} placed: ID {order['orderId']}, Status: {order['status']}")

            if i < num_slices - 1:
                time.sleep(interval)

        print("✅ TWAP Execution Completed.")

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        print(f"Error: {ve}")
    except BinanceAPIException as api_exc:
        logger.error(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
        print(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
    except Exception as e:
        logger.critical(f"Unexpected error in TWAP: {e}", exc_info=True)
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TWAP Order Executor")
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True)
    parser.add_argument("--total_quantity", type=float, required=True)
    parser.add_argument("--num_slices", type=int, required=True)
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], default="MARKET")

    args = parser.parse_args()

    place_twap_orders(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        total_quantity=args.total_quantity,
        num_slices=args.num_slices,
        interval=args.interval,
        order_type=args.type.upper()
    )
