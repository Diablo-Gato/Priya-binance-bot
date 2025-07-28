# src/advanced/grid.py

import argparse
from decimal import Decimal
from binance.exceptions import BinanceAPIException
from src.utils.api import get_binance_client
from src.utils.logger import setup_logger
from src.utils.account import has_sufficient_balance
from src.utils.validation import validate_order_params

logger = setup_logger()
client = get_binance_client()

def place_grid_orders(symbol: str, side: str, total_quantity: float, lower_price: float, upper_price: float, grid_count: int):
    """
    Places a grid of LIMIT orders equally spaced between lower_price and upper_price.

    Args:
        symbol (str): Trading pair symbol (e.g., BTCUSDT)
        side (str): 'BUY' or 'SELL'
        total_quantity (float): Total quantity to be split across grid orders
        lower_price (float): Lower bound of grid
        upper_price (float): Upper bound of grid
        grid_count (int): Number of grid orders
    """
    try:
        if grid_count < 2:
            raise ValueError("Grid count must be at least 2")

        step = (upper_price - lower_price) / (grid_count - 1)
        slice_quantity = round(total_quantity / grid_count, 6)

        logger.info(f"Placing {grid_count} grid orders from {lower_price} to {upper_price} with step {step:.2f}")

        for i in range(grid_count):
            price = round(lower_price + (i * step), 2)

            validate_order_params(client, symbol, slice_quantity, price)

            if not has_sufficient_balance(client, symbol, side, slice_quantity, price):
                raise ValueError(f"Insufficient balance for grid order {i+1} at price {price}")

            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=slice_quantity,
                price=str(price),
                timeInForce="GTC"
            )

            logger.info(f"Grid Order {i+1}: ID {order['orderId']}, Price: {price}, Qty: {slice_quantity}, Status: {order['status']}")
            print(f"✅ Grid Order {i+1}/{grid_count}: Price: {price}, Order ID: {order['orderId']}, Status: {order['status']}")

        print("✅ Grid Execution Completed.")

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        print(f"Error: {ve}")
    except BinanceAPIException as api_exc:
        logger.error(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
        print(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
    except Exception as e:
        logger.critical(f"Unexpected error in Grid: {e}", exc_info=True)
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grid Trading Bot")
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True)
    parser.add_argument("--total_quantity", type=float, required=True)
    parser.add_argument("--lower_price", type=float, required=True)
    parser.add_argument("--upper_price", type=float, required=True)
    parser.add_argument("--grid_count", type=int, required=True)

    args = parser.parse_args()

    place_grid_orders(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        total_quantity=args.total_quantity,
        lower_price=args.lower_price,
        upper_price=args.upper_price,
        grid_count=args.grid_count
    )
