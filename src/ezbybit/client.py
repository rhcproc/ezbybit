from decimal import Decimal, ROUND_DOWN

from pybit.unified_trading import HTTP


class BybitClient:
    QUOTE_COIN = "USDT"
    DEFAULT_BUDGET_RATIO = Decimal("0.8")
    SUPPORTED_BASE_COINS = {"BTC", "ETH"}

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.session = HTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )

    @staticmethod
    def truncate(number, digits) -> float:
        quantizer = Decimal("1").scaleb(-digits)
        return float(
            Decimal(str(number)).quantize(
                quantizer,
                rounding=ROUND_DOWN,
            )
        )

    @classmethod
    def normalize_coin(cls, coin: str) -> str:
        coin = coin.upper()
        if coin in cls.SUPPORTED_BASE_COINS or coin == cls.QUOTE_COIN:
            return coin
        raise ValueError(f"Unsupported coin: {coin}. Use BTC or ETH.")

    @classmethod
    def get_symbol(cls, coin: str) -> str:
        return f"{cls.normalize_coin(coin)}{cls.QUOTE_COIN}"

    def get_coin_info(self, coin: str) -> dict:
        coin = self.normalize_coin(coin)
        result = self.session.get_wallet_balance(
            accountType="UNIFIED",
            coin=coin,
        )["result"]
        coins = result["list"][0]["coin"]
        return next((item for item in coins if item["coin"] == coin), {})

    def get_available_coin_amount(self, coin: str) -> Decimal:
        coin_info = self.get_coin_info(coin)

        if coin_info.get("free") not in (None, ""):
            return Decimal(coin_info["free"])

        wallet_balance = Decimal(coin_info.get("walletBalance") or "0")
        locked = Decimal(coin_info.get("locked") or "0")
        spot_borrow = Decimal(coin_info.get("spotBorrow") or "0")
        return max(wallet_balance - locked - spot_borrow, Decimal("0"))

    def get_available_budget_usdt(
        self,
        budget_ratio: Decimal = DEFAULT_BUDGET_RATIO,
    ) -> float:
        budget = self.get_available_coin_amount(self.QUOTE_COIN) * budget_ratio
        return self.truncate(budget, 2)

    def buy(
        self,
        coin: str,
        budget_ratio: Decimal = DEFAULT_BUDGET_RATIO,
    ) -> dict:
        qty = self.get_available_budget_usdt(budget_ratio)
        return self.session.place_order(
            category="spot",
            symbol=self.get_symbol(coin),
            side="Buy",
            orderType="Market",
            qty=str(qty),
        )

    def buy_btc(self) -> dict:
        return self.buy("BTC")

    def buy_eth(self) -> dict:
        return self.buy("ETH")

    @staticmethod
    def get_decimal(value) -> int:
        value = str(value)
        if "." in value:
            return len(value.split(".")[1])
        return 0

    def get_spot_symbol_decimal(self, coin: str) -> int:
        result = self.session.get_orderbook(
            category="spot",
            symbol=self.get_symbol(coin),
        )["result"]
        decimal_a = self.get_decimal(result["a"][0][1])
        decimal_b = self.get_decimal(result["b"][0][1])
        return max(decimal_a, decimal_b)

    def get_sellable_quantity(self, coin: str) -> float:
        coin = self.normalize_coin(coin)
        decimal = self.get_spot_symbol_decimal(coin)
        return self.truncate(self.get_available_coin_amount(coin), decimal)

    def get_sellable_quantity_btc(self) -> float:
        return self.get_sellable_quantity("BTC")

    def get_sellable_quantity_eth(self) -> float:
        return self.get_sellable_quantity("ETH")

    def sell(self, coin: str) -> dict:
        qty = self.get_sellable_quantity(coin)
        return self.session.place_order(
            category="spot",
            symbol=self.get_symbol(coin),
            side="Sell",
            orderType="Market",
            qty=str(qty),
        )

    def sell_btc(self) -> dict:
        return self.sell("BTC")

    def sell_eth(self) -> dict:
        return self.sell("ETH")
