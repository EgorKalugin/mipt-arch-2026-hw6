import logging

from converters import UsdEurConverter, UsdGbpConverter, UsdRubConverter, UsdCnyConverter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main() -> None:
    try:
        amount = float(input("Введите значение в USD: "))
    except ValueError:
        print("Ошибка: введите корректное число.")
        return

    converters = [
        ("RUB", UsdRubConverter()),
        ("EUR", UsdEurConverter()),
        ("GBP", UsdGbpConverter()),
        ("CNY", UsdCnyConverter()),
    ]

    for currency, converter in converters:
        print(f"{amount} USD -> {currency}: {converter.convert(amount):.2f}")


if __name__ == "__main__":
    main()
