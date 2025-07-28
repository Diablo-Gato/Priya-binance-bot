import argparse
from binance.exceptions import BinanceAPIException
from src.utils.api import get_binance_client
from src.utils.logger import setup_logger
from src.utils.account import has_sufficient_balance
from src.utils.validation import validate_order_params

logger = setup_logger()
client = get_binance_client()

def place_oco_orders(symbol: str, side: str, quantity: float, tp_price: float, stop_price: float, stop_limit_price: float):
    """
    Simulates OCO (One-Cancels-the-Other) orders on Binance Futures.
    Places a LIMIT order for take-profit and a STOP-MARKET order for stop-loss.

    Args:
        symbol (str): Trading pair symbol (e.g., BTCUSDT).
        side (str): Order side ('BUY' or 'SELL') for both orders.
        quantity (float): Quantity to trade for both orders.
        tp_price (float): Take-Profit limit price.
        stop_price (float): Stop trigger price for the stop-market order.
        stop_limit_price (float): (Unused in STOP_MARKET) Reserved for STOP_LIMIT support.
    """
    try:
        validate_order_params(client, symbol, quantity, tp_price)
        validate_order_params(client, symbol, quantity, stop_price)

        if not has_sufficient_balance(client, symbol, side, quantity, max(tp_price, stop_price)):
            raise ValueError("Insufficient balance for OCO order.")

        # Place Take-Profit LIMIT order
        limit_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=str(tp_price),
            timeInForce="GTC"
        )
        logger.info(f"Take-Profit LIMIT order placed. ID: {limit_order['orderId']}, Price: {tp_price}")

        # Place Stop-MARKET order
        stop_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            stopPrice=str(stop_price),
            quantity=quantity,
            workingType="MARK_PRICE"
        )
        logger.info(f"Stop-MARKET order placed. ID: {stop_order['orderId']}, Stop: {stop_price}")

        print(f"✅ OCO simulated: LIMIT Order ID: {limit_order['orderId']}, STOP-MARKET Order ID: {stop_order['orderId']}")

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        print(f"Error: {ve}")
    except BinanceAPIException as api_exc:
        logger.error(f"Binance API Error (Code: {api_exc.code}): {api_exc.message}")
        print(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")
    except Exception as e:
        logger.critical(f"Unexpected error placing OCO orders: {e}", exc_info=True)
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate OCO order on Binance Futures")
    parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("tp_price", type=float, help="Take-Profit price")
    parser.add_argument("stop_price", type=float, help="Stop trigger price")
    parser.add_argument("stop_limit_price", type=float, help="Stop limit execution price (unused)")

    args = parser.parse_args()

    place_oco_orders(
        args.symbol.upper(),
        args.side.upper(),
        args.quantity,
        args.tp_price,
        args.stop_price,
        args.stop_limit_price
    )