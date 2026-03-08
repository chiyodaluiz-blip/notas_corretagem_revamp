def parse_number(x):

    x = x.replace(".", "")
    x = x.replace(",", ".")

    return float(x)


def parse_trade_line(line):

    if not line.startswith("BOVESPA"):
        return None

    tokens = line.split()

    if len(tokens) < 8:
        return None

    try:

        side = tokens[1]
        asset = tokens[3]

        qty = parse_number(tokens[5])
        price = parse_number(tokens[6])

        return {
            "asset": asset,
            "side": side,
            "qty": qty,
            "price": price
        }

    except:
        return None
