import streamlit as st
import pandas as pd
from utils.salvar import salvar_pontos
from datetime import datetime
import os

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🏱 Recompensas")

    caminho_resgates = "data/resgates.csv"
    if not os.path.exists(caminho_resgates):
        pd.DataFrame(columns=["Data", "Recompensa", "Pontos"]).to_csv(caminho_resgates, index=False)

    resgates_df = pd.read_csv(caminho_resgates)
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
            if pontos_disponiveis >= row["Pontos"]:
                if st.button("✨ Resgatar", key=f"resgatar_{i}_{datetime.now().timestamp()}"):
                    st.session_state.pontos_totais -= row["Pontos"]
                    salvar_pontos()

                    novo_resgate = {
                        "Data": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        "Recompensa": row["Nome"],
                        "Pontos": row["Pontos"]
                    }
                    resgates_df = resgates_df.append(novo_resgate, ignore_index=True)
                    resgates_df.to_csv(caminho_resgates, index=False)
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos")
