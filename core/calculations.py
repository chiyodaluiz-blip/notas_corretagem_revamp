import pandas as pd
import numpy as np


def apply_pro_rata(note):

    trades = note.trades
    taxes = note.taxes

    rows = []

    for t in trades:

        rows.append({
            "asset": t.asset,
            "side": t.side,
            "qty": t.quantity,
            "price": t.price
        })

    df = pd.DataFrame(rows)

    df["valor"] = df.qty * df.price

    total_valor = df.valor.sum()

    ratio = df.valor / total_valor

    df["tx_liq"] = taxes.liquidacao * ratio
    df["tx_reg"] = taxes.registro * ratio
    df["emol"] = taxes.emolumentos * ratio
    df["tx_op"] = taxes.operacional * ratio
    df["impostos"] = taxes.impostos * ratio

    df["fees"] = df[["tx_liq","tx_reg","emol","tx_op","impostos"]].sum(axis=1)

    df["valor_pago"] = np.where(
        df.side == "C",
        df.valor + df.fees,
        df.valor - df.fees
    )

    return df