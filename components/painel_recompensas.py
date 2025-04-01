# components/painel_recompensas.py

import streamlit as st
import pandas as pd

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🎁 Suas Recompensas")

    recompensas = pd.read_csv("data/recompensas.csv")

    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<span style='font-size:48px'>{row['Emoji']}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"### {row['Nome']}")
            st.markdown(f"🪙 **{row['Pontos']} pontos**")
            if pontos_disponiveis >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos para liberar")
