import streamlit as st
import pandas as pd

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🎁 TESTE Recompensas")

    recompensas = pd.read_csv("data/recompensas.csv")

    cores_borda = {
        "Pequena": "#A8E6CF",
        "Média": "#AEDFF7",
        "Grande": "#D1C4E9",
        "Épica": "#F9D5E5"
    }

    for i, row in recompensas.iterrows():
        cor_borda = cores_borda.get(row["Tipo"], "#CCCCCC")
        estilo_caixa = f"""
            border: 3px solid {cor_borda};
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
        """

        with st.container():
            st.markdown(f"<div style='{estilo_caixa}'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"<h2 style='margin: 0;'>{row['Emoji']}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"### {row['Nome']}")
                st.markdown(f"🪙 **{row['Pontos']} pontos**")
                if pontos_disponiveis >= row["Pontos"]:
                    if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                        st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
                else:
                    st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos para liberar")
            st.markdown("</div>", unsafe_allow_html=True)
