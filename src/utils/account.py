from src.utils.api import get_binance_client
import logging

client = get_binance_client()
logger = logging.getLogger("BinanceBot")

def has_sufficient_balance(client, symbol: str, side: str, quantity: float, price: float) -> bool:
    """
    Check if the user has sufficient USDT balance to place the order.

    Args:
        client: Binance client
        symbol (str): Trading pair symbol (e.g., BTCUSDT).
        side (str): Order side (BUY or SELL)
        quantity (float): Quantity to buy/sell.
        price (float): Price per unit.

    Returns:
        bool: True if sufficient balance, False otherwise.
    """
    try:
        balance_data = client.futures_account_balance()
        usdt_balance = next(item for item in balance_data if item['asset'] == 'USDT')
        available_balance = float(usdt_balance['balance'])
        required = quantity * price

        logger.debug(f"Checking balance: required={required}, available={available_balance}")
        return available_balance >= required
    except Exception as e:
        logger.error(f"Balance check error for {symbol}: {e}", exc_info=True)
        return False