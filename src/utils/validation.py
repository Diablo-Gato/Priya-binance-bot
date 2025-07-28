from decimal import Decimal, getcontext

getcontext().prec = 10

def validate_order_params(client, symbol, quantity, price=None):
    exchange_info = client.futures_exchange_info()
    symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

    if not symbol_info:
        raise ValueError(f"Invalid symbol: {symbol}")

    min_qty = float(next(f['minQty'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'))
    step_size = float(next(f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'))

    if quantity < min_qty:
        raise ValueError(f"Quantity {quantity} is less than minimum allowed ({min_qty}) for {symbol}.")

    quantity_dec = Decimal(str(quantity))
    min_qty_dec = Decimal(str(min_qty))
    step_size_dec = Decimal(str(step_size))
    qdiff = (quantity_dec - min_qty_dec) / step_size_dec
    if qdiff != qdiff.to_integral_value():
        raise ValueError(f"Quantity {quantity} does not adhere to step size ({step_size}) for {symbol}.")

    if price is not None:
        min_price = float(next(f['minPrice'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'))
        tick_size = float(next(f['tickSize'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'))

        price_dec = Decimal(str(price))
        min_price_dec = Decimal(str(min_price))
        tick_size_dec = Decimal(str(tick_size))
        diff = (price_dec - min_price_dec) / tick_size_dec
        if diff != diff.to_integral_value():
            raise ValueError(f"Price {price} does not adhere to tick size ({tick_size}) for {symbol}.")

    return True
