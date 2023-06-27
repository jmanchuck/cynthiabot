def currency_string(value: str, currency_id: str) -> str:
    symbol = ""
    if currency_id == "USD":
        symbol = "$"
    elif currency_id == "GBP":
        symbol = "£"
    elif currency_id == "EUR":
        symbol = "€"

    if symbol:
        return symbol + value

    return f"{value} {currency_id}"
