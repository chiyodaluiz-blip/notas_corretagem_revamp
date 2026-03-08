import re

TICKER_REGEX = r"[A-Z]{4}\d{1,2}"


def is_number(token):

    token = token.replace(".", "").replace(",", ".")

    try:
        float(token)
        return True
    except:
        return False


def parse_trade_line(line):

    tokens = line.split()

    ticker = None
    side = None
    qty = None
    price = None

    # detectar ticker
    for t in tokens:
        if re.match(TICKER_REGEX, t):
            ticker = t
            break

    # detectar lado
    for t in tokens:
        if t in ["C", "V"]:
            side = t
            break

    # detectar números
    numbers = []

    for t in tokens:

        if is_number(t):
            numbers.append(t)

    if len(numbers) >= 2:

        qty = float(numbers[0].replace(",", "."))
        price = float(numbers[-1].replace(",", "."))

    if ticker and side and qty and price:

        return {
            "asset": ticker,
            "side": side,
            "qty": qty,
            "price": price
        }

    return None