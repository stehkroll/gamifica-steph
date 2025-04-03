import streamlit as st
import pandas as pd
from utils.salvar import salvar_pontos
from datetime import datetime
import os

def mostrar_painel_recompensas(_):
    st.subheader("🎁 Recompensas")

    # Garante que a pasta data exista
    os.makedirs("data", exist_ok=True)

    # Garante que o arquivo de resgates exista
    if not os.path.exists("data/resgates.csv"):
        pd.DataFrame(columns=["Data", "Recompensa", "Pontos"]).to_csv("data/resgates.csv", index=False)

    recompensas = pd.read_csv("data/recompensas.csv")
    recompensas.columns = recompensas.columns.str.strip()

    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h3 style='font-size: 18px; margin: 0;'>{row['Nome']} {row['Emoji']}</h3>", unsafe_allow_html=True)
        with col2:
            if st.session_state.pontos_totais >= row["Pontos"]:
                if st.button(f"✨ Resgatar ", key=f"resgatar_{i}_{datetime.now().timestamp()}"):
                    st.session_state.pontos_totais -= row["Pontos"]
                    salvar_pontos()

                    # Salva o resgate
                    novo = pd.DataFrame([{
                        "Data": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                        "Recompensa": row["Nome"],
                        "Pontos": row["Pontos"]
                    }])
                    novo.to_csv("data/resgates.csv", mode='a', header=False, index=False)

                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - st.session_state.pontos_totais} pontos")
