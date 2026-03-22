from .currency_converter import CurrencyConverter
from .rate_fetcher import fetch_rates


class BaseUsdConverter(CurrencyConverter):
    currency: str

    def __init__(self) -> None:
        self.rates = fetch_rates()

    def convert(self, amount: float) -> float:
        if self.rates is None:
            raise RuntimeError("Exchange rates unavailable")
        return amount * self.rates[self.currency]
