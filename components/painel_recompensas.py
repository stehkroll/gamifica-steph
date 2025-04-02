import streamlit as st
import pandas as pd
from utils.salvar import salvar_pontos  # <-- agora importa do novo arquivo

def mostrar_painel_recompensas(_):
    st.subheader("🎁 Recompensas")

    recompensas = pd.read_csv("data/recompensas.csv")
    recompensas.columns = recompensas.columns.str.strip()

    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h3 style='font-size: 18px; margin: 0;'>{row['Nome']} {row['Emoji']}</h3>", unsafe_allow_html=True)

        with col2:
            if st.session_state.pontos_totais >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    st.session_state.pontos_totais -= row["Pontos"]
                    salvar_pontos()
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")

            else:
                st.info(f"🔒 Faltam {row['Pontos'] - st.session_state.pontos_totais} pontos")
