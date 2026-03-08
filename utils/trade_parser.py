import re

TICKER_REGEX = r"[A-Z]{4}\d{1,2}"


def parse_number(token):

    token = token.strip()
    token = token.replace(".", "")
    token = token.replace(",", ".")

    return float(token)


def is_number(token):

    try:
        parse_number(token)
        return True
    except:
        return False


def parse_trade_line(line):

    tokens = line.split()

    ticker = None
    side = None
    qty = None
    price = None

    for t in tokens:
        if re.match(TICKER_REGEX, t):
            ticker = t
            break

    for t in tokens:
        if t in ["C", "V"]:
            side = t
            break

    numbers = []

    for t in tokens:

        if is_number(t):
            numbers.append(t)

    if len(numbers) >= 2:

        qty = parse_number(numbers[0])
        price = parse_number(numbers[-1])

    if ticker and side and qty and price:

        return {
            "asset": ticker,
            "side": side,
            "qty": qty,
            "price": price
        }

    return None
