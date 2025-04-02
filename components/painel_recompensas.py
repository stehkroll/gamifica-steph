import streamlit as st
import pandas as pd

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🎁 Recompensas")

    recompensas = pd.read_csv("data/recompensas.csv")

    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(f"assets/recompensas/{row['Imagem']}", width=64)
        with col2:
            st.markdown(f"### {row['Nome']}")
            st.markdown(f"🪙 **{row['Pontos']} pontos**")
            if pontos_disponiveis >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos para liberar")
