import streamlit as st
import pandas as pd
from utils.salvar import salvar_pontos
from datetime import datetime
import os

def mostrar_painel_recompensas():
    st.subheader("🎁 Recompensas")

    caminho_resgates = "data/resgates.csv"
    caminho_progresso = "data/progresso.csv"

    if not os.path.exists(caminho_resgates):
        pd.DataFrame(columns=["Data", "Recompensa", "Pontos"]).to_csv(caminho_resgates, index=False)

    if not os.path.exists(caminho_progresso):
        pd.DataFrame(columns=["Data", "Pontos", "Nivel"]).to_csv(caminho_progresso, index=False)

    try:
        resgates_df = pd.read_csv(caminho_resgates)
    except pd.errors.EmptyDataError:
        resgates_df = pd.DataFrame(columns=["Data", "Recompensa", "Pontos"])

    try:
        progresso_df = pd.read_csv(caminho_progresso)
    except pd.errors.EmptyDataError:
        progresso_df = pd.DataFrame(columns=["Data", "Pontos", "Nivel"])

    recompensas = pd.read_csv("data/recompensas.csv")
    recompensas.columns = recompensas.columns.str.strip()

    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(
                f"<h3 style='font-size: 18px; margin: 0;'>{row['Emoji']}</h3>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='font-size:16px; margin-bottom:5px;'><strong>{row['Nome']}</strong> – {row['Pontos']} pts</div>",
                unsafe_allow_html=True
            )

            if st.session_state.pontos_totais >= row["Pontos"]:
                if st.button("✨ Resgatar", key=f"resgatar_{row['Nome']}_{datetime.now().timestamp()}"):
                    st.session_state.pontos_totais -= row["Pontos"]
                    salvar_pontos()

                    novo_resgate = {
                        "Data": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        "Recompensa": row["Nome"],
                        "Pontos": row["Pontos"]
                    }
                    resgates_df = pd.concat([resgates_df, pd.DataFrame([novo_resgate])], ignore_index=True)
                    resgates_df.to_csv(caminho_resgates, index=False)

                    # Também salva progresso negativo para o controle correto do XP
                    novo_progresso = {
                        "Data": datetime.today().strftime('%Y-%m-%d'),
                        "Pontos": 0,  # Recompensas não adicionam XP
                        "Nivel": "-"
                    }
                    progresso_df = pd.concat([progresso_df, pd.DataFrame([novo_progresso])], ignore_index=True)
                    progresso_df.to_csv(caminho_progresso, index=False)

                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - st.session_state.pontos_totais} pontos")
