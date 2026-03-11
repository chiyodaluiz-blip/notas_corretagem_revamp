import pandas as pd
import numpy as np


def apply_pro_rata(note):

    rows = []

    for t in note.trades:

        rows.append({
            "asset": t.asset,
            "side": t.side,
            "qty": t.quantity,
            "price": t.price
        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df["valor"] = df["qty"] * df["price"]

    total_valor = df["valor"].sum()

    ratio = df["valor"] / total_valor

    taxes = note.taxes

    df["tx_liq"] = taxes.liquidacao * ratio
    df["tx_reg"] = taxes.registro * ratio
    df["emol"] = taxes.emolumentos * ratio
    df["tx_op"] = taxes.operacional * ratio
    df["impostos"] = taxes.impostos * ratio
    df["irrf"] = taxes.irrf * ratio

    df["fees"] = df[["tx_liq","tx_reg","emol","tx_op","impostos","irrf"]].sum(axis=1)

    df["valor_pago"] = np.where(
        df["side"] == "C",
        df["valor"] + df["fees"],
        df["valor"] - df["fees"]
    )

    # Signed version: buys are negative (debit), sells are positive (credit)
    df["valor_pago_sign"] = df["valor_pago"]
    df.loc[df["side"] == "C", "valor_pago_sign"] = df.loc[df["side"] == "C", "valor_pago_sign"] * -1

    return df

def validate_note(df, note):

    if note.liquido_para is None:
        return None

    valor_calculado = df["valor_pago_sign"].sum()

    diff = abs(abs(note.liquido_para) - abs(valor_calculado))

    return diff
