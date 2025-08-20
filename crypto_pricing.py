import requests
import argparse
import time
from decimal import Decimal, ROUND_HALF_UP

def decor_rate_limiter(min_seconds):
    def wrapper_function(func):
        last_time = {"t": 0}
        last_result = {"v": None}

        def inner(*args, **kwargs):
            now = time.monotonic()
            # recently called values
            if now - last_time["t"] < min_seconds and last_result["v"] is not None:
                return last_result["v"]

            # otherwise this will store the result
            result = func(*args, **kwargs)
            last_time["t"] = now
            last_result["v"] = result
            return result

        return inner
    return wrapper_function


@decor_rate_limiter(2)
def fetch_coinbase_data():
    url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
    response = requests.get(url, timeout=10)
    data = response.json()

    bids = [ls[:2] for ls in data["bids"]]
    asks = [ls[:2] for ls in data["asks"]]

    return {"bids": bids,"asks": asks}


@decor_rate_limiter(2)
def fetch_gemini_data():
    url = "https://api.gemini.com/v1/book/BTCUSD"
    response = requests.get(url, timeout=10)
    data = response.json()

    bids = [[b["price"], b["amount"]] for b in data["bids"]]
    asks = [[a["price"], a["amount"]] for a in data["asks"]]

    return {"bids": bids,"asks": asks}


def calculate_price(qty, orders):
    remaining = qty
    total_usd = Decimal("0")

    for price, size in orders:
        take = min(remaining, size)
        if take > 0:
            total_usd += price * take
            remaining -= take
        if remaining <= 0:
            break

    return total_usd


def usd_format(amount):
    return f"{amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qty", type=Decimal, default=Decimal("10"))
    args = parser.parse_args()

    coinbase = fetch_coinbase_data()
    gemini = fetch_gemini_data()

    # merging the exchanges
    all_bids, all_asks = [], []
    for book in [coinbase, gemini]:
        all_bids.extend((Decimal(p), Decimal(s)) for p, s in book["bids"])
        all_asks.extend((Decimal(p), Decimal(s)) for p, s in book["asks"])

    bids_sorted_values  = sorted(all_bids, key=lambda x: x[0], reverse=True)
    bids = [list(st) for st in bids_sorted_values]

    asks_sorted_values = sorted(all_asks, key=lambda x: x[0])
    asks = [list(st) for st in asks_sorted_values]

    #buy and sell calculation
    buy_cost = calculate_price(args.qty, asks)
    sell_revenue = calculate_price(args.qty, bids)

    print(f"To buy {args.qty} BTC: ${usd_format(buy_cost)}")
    print(f"To sell {args.qty} BTC: ${usd_format(sell_revenue)}")


if __name__ == "__main__":
    main()
