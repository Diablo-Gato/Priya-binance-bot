import argparse
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.oco_orders import place_oco_orders

def main():
    parser = argparse.ArgumentParser(description="Binance Futures CLI Bot")
    parser.add_argument("--type", required=True, choices=["market", "limit", "oco"], help="Type of order to place")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")

    # Optional for Limit and OCO
    parser.add_argument("--price", type=float, help="Limit order price")
    parser.add_argument("--tp", type=float, help="Take-Profit price for OCO")
    parser.add_argument("--stop", type=float, help="Stop trigger price for OCO")
    parser.add_argument("--sl", type=float, help="Stop-limit execution price for OCO")

    args = parser.parse_args()

    symbol = args.symbol.upper()
    side = args.side.upper()

    if args.type == "market":
        place_market_order(symbol, side, args.quantity)

    elif args.type == "limit":
        if not args.price:
            print("❌ Price required for limit order.")
            return
        place_limit_order(symbol, side, args.quantity, args.price)

    elif args.type == "oco":
        if not all([args.tp, args.stop, args.sl]):
            print("❌ For OCO, you must provide --tp (take-profit), --stop (trigger), and --sl (stop-limit).")
            return
        place_oco_orders(symbol, side, args.quantity, args.tp, args.stop, args.sl)

if __name__ == "__main__":
    main()
