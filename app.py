import streamlit as st
import tempfile
import os
import pandas as pd

from core.pipeline import process_notes


st.set_page_config(
    page_title="Processador de Notas de Corretagem",
    layout="wide"
)

st.title("📄 Processador de Notas de Corretagem B3")

uploaded = st.file_uploader(
    "Upload das notas",
    type="pdf",
    accept_multiple_files=True
)


if uploaded and st.button("Processar"):

    progress = st.progress(0)

    logs = []

    def log_callback(msg):
        logs.append(msg)

    with tempfile.TemporaryDirectory() as tmp:

        files = []

        for f in uploaded:

            path = os.path.join(tmp, f.name)

            with open(path, "wb") as out:
                out.write(f.getbuffer())

            files.append(path)

        def update_progress(p):
            progress.progress(int(p * 100))

        df = process_notes(
            files,
            progress_callback=update_progress,
            status_callback=log_callback
        )

    st.success("✅ Processamento concluído")

    # ======================
    # LOGS DO PROCESSAMENTO
    # ======================

    with st.expander("📋 Logs do processamento", expanded=True):

        for l in logs:
            st.write(l)

    # ======================
    # RESUMO GERAL
    # ======================

    if not df.empty:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Trades",
            len(df)
        )

        col2.metric(
            "Ativos únicos",
            df["asset"].nunique() if "asset" in df else 0
        )

        col3.metric(
            "Valor negociado",
            f"R$ {df['valor'].sum():,.2f}" if "valor" in df else "-"
        )

        col4.metric(
            "Total taxas",
            f"R$ {df['fees'].sum():,.2f}" if "fees" in df else "-"
        )

    st.divider()

    # ======================
    # TABELA RESULTADO
    # ======================

    st.subheader("Trades processados")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ======================
    # DOWNLOAD
    # ======================

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False),
        "trades_processados.csv"
    )
