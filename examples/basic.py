import os
from ezbybit import BybitClient


api_key = os.environ["BYBIT_API_KEY"]
api_secret = os.environ["BYBIT_API_SECRET"]


if __name__ == "__main__":
    client = BybitClient(
        api_key=api_key,
        api_secret=api_secret,
        testnet=False,
    )

    print(client.get_available_budget_usdt())
    print(client.get_sellable_quantity_btc())
    print(client.get_sellable_quantity_eth())
    # res = client.buy("ETH", Decimal("0.5"))
    # print(res)
    # res = client.sell("ETH")
    # print(res)
