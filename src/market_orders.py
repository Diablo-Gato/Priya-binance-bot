import argparse
from decimal import Decimal, getcontext
from src.utils.api import get_binance_client
from src.utils.logger import setup_logger
from binance.exceptions import BinanceAPIException

# Set precision for Decimal calculations
getcontext().prec = 10

logger = setup_logger()

def validate_order_params(client, symbol: str, quantity: float, price: float = None) -> bool:
    """
    Validate the trading symbol, quantity, and (optional) price against Binance Futures constraints.
    """
    exchange_info = client.futures_exchange_info()
    symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

    if not symbol_info:
        raise ValueError(f"Invalid symbol: {symbol}. Please check Binance Futures API for valid symbols.")

    # LOT_SIZE filter (quantity validation)
    min_qty = float(next(f['minQty'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'))
    step_size = float(next(f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'))

    quantity_dec = Decimal(str(quantity))
    min_qty_dec = Decimal(str(min_qty))
    step_size_dec = Decimal(str(step_size))

    if quantity < min_qty:
        raise ValueError(f"Quantity {quantity} is less than minimum allowed ({min_qty}) for {symbol}.")

    if ((quantity_dec - min_qty_dec) / step_size_dec) % 1 != 0:
        raise ValueError(f"Quantity {quantity} does not adhere to step size ({step_size}) for {symbol}.")

    # PRICE_FILTER (if price is provided)
    if price is not None:
        min_price = float(next(f['minPrice'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'))
        tick_size = float(next(f['tickSize'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'))

        price_dec = Decimal(str(price))
        min_price_dec = Decimal(str(min_price))
        tick_size_dec = Decimal(str(tick_size))

        if price < min_price:
            raise ValueError(f"Price {price} is less than minimum allowed ({min_price}) for {symbol}.")

        if ((price_dec - min_price_dec) / tick_size_dec) % 1 != 0:
            raise ValueError(f"Price {price} does not adhere to tick size ({tick_size}) for {symbol}.")

    return True

def place_market_order(symbol: str, side: str, quantity: float) -> None:
    """
    Places a market order on Binance Futures.
    """
    client = get_binance_client()
    try:
        validate_order_params(client, symbol, quantity)

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        logger.info(
            f"Market order placed successfully. ID: {order['orderId']}, "
            f"Symbol: {order['symbol']}, Side: {order['side']}, "
            f"Quantity: {order['origQty']}, Status: {order['status']}"
        )
        print(f"✅ Success: Market order placed. Order ID: {order['orderId']}, Status: {order['status']}")

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        print(f"Error: {ve}")

    except BinanceAPIException as api_exc:
        logger.error(f"Binance API Error (Code: {api_exc.code}): {api_exc.message}")
        print(f"Binance API Error: {api_exc.message} (Code: {api_exc.code})")

    except Exception as e:
        logger.critical(f"Unexpected error placing market order: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a market order")
    parser.add_argument("symbol", type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    args = parser.parse_args()

    place_market_order(args.symbol.upper(), args.side.upper(), args.quantity)
