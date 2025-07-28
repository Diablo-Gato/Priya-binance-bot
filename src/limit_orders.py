import argparse
from binance.exceptions import BinanceAPIException
from src.utils.api import get_binance_client
from src.utils.logger import setup_logger
from src.utils.account import has_sufficient_balance
from src.utils.validation import validate_order_params

logger = setup_logger()
client = get_binance_client()

def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Place a LIMIT order on Binance Futures.

    Args:
        symbol (str): Trading pair (e.g., BTCUSDT)
        side (str): BUY or SELL
        quantity (float): Order quantity
        price (float): Limit price
    """
    try:
        validate_order_params(client, symbol, quantity, price)

        if not has_sufficient_balance(client, symbol, side, quantity, price):
            raise ValueError("Insufficient balance to place limit order.")

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        logger.info(
            f"Limit order placed successfully. ID: {order['orderId']}, "
            f"Symbol: {order['symbol']}, Side: {order['side']}, "
            f"Quantity: {order['origQty']}, Price: {order['price']}, Status: {order['status']}"
        )
        print(f"Success: Limit order placed. Order ID: {order['orderId']}, Status: {order['status']}")

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        print(f"Error: {ve}")
    except BinanceAPIException as api_exc:
        logger.error(f"Binance API Error placing limit order (Code: {api_exc.code}): {api_exc.message}")
        print(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
    except Exception as e:
        logger.critical(f"Unexpected error placing limit order: {e}", exc_info=True)
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a limit order")
    parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("price", type=float, help="Limit price")
    args = parser.parse_args()

    place_limit_order(args.symbol.upper(), args.side.upper(), args.quantity, args.price)
