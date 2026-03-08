import streamlit as st
import tempfile
import os

from core.pipeline import process_notes

st.title("Processador de Notas de Corretagem B3")

uploaded = st.file_uploader(
    "Upload das notas",
    type="pdf",
    accept_multiple_files=True
)

if uploaded:

    progress = st.progress(0)
    status = st.empty()

    with tempfile.TemporaryDirectory() as tmp:

        files = []

        for f in uploaded:
            path = os.path.join(tmp, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            files.append(path)

        def update_progress(p):
            progress.progress(int(p*100))

        df = process_notes(
            files,
            progress_callback=update_progress,
            status_callback=lambda x: status.info(x)
        )

    st.success("Processamento concluído")

    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "trades_processados.csv"
    )