import pandas as pd

from brokers.b3_parser import B3Parser
from core.calculations import apply_pro_rata, validate_note
from utils.pdf_text import extract_text
from utils.broker_detection import detect_broker


def process_notes(files, progress_callback=None, status_callback=None):

    parser = B3Parser()

    all_results = []

    total = len(files)

    for i, f in enumerate(files):

        text = extract_text(f)

        broker = detect_broker(text)

        if status_callback:
            status_callback(f"{f} | corretora detectada: {broker}")

        note = parser.parse_from_text(text)

        df = apply_pro_rata(note)

        df["date"] = note.date
        df["broker"] = broker

        diff = validate_note(df, note)
        
        if status_callback:
        
            assets = sorted(df["asset"].unique())
        
            total_trades = len(df)
        
            total_valor = df["valor"].sum()
        
            total_fees = df["fees"].sum()
        
            status_callback(
                f"""
        📄 **Arquivo:** {f}
        
        📅 **Data:** {note.date}
        
        🏦 **Corretora:** {broker}
        
        📊 **Trades:** {total_trades}
        
        📈 **Ativos:** {", ".join(assets)}
        
        💰 **Valor bruto negociado:** R$ {total_valor:,.2f}
        
        🧾 **Total taxas:** R$ {total_fees:,.2f}
        """
            )

        if status_callback:
        
            if diff is not None and diff > 1:
        
                status_callback(
                    f"❌ **Validação falhou** — diferença: R$ {diff:.2f}"
                )
        
            else:
        
                status_callback(
                    "✅ **Validação financeira OK**"
                )
                
        all_results.append(df)

        if progress_callback:
            progress_callback((i + 1) / total)

    if len(all_results) == 0:
        return pd.DataFrame()

    return pd.concat(all_results, ignore_index=True)
