from .currency_converter import CurrencyConverter
from .rate_fetcher import fetch_rates_cached


class UsdCnyConverter(CurrencyConverter):
    def __init__(self, cache_file: str = "exchange_rates.json", cache_expiry: int = 3600) -> None:
        self.rates = fetch_rates_cached(cache_file, cache_expiry)

    def convert(self, amount: float) -> float:
        if self.rates is None:
            raise RuntimeError("Exchange rates unavailable")
        return amount * self.rates["CNY"]
