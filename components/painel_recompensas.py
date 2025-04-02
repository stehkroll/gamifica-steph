import streamlit as st
import pandas as pd

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🎁 Suas Recompensas")

    # Carrega as recompensas do CSV
    recompensas = pd.read_csv("data/recompensas.csv")

    for i, row in recompensas.iterrows():
        # Ajustando para 5 colunas
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
        
        with col1:
            # Exibe o nome da recompensa com o emoji ao lado
            st.markdown(f"### {row['Nome']} {row['Emoji']}")  # Nome + Emoji
        
        with col2:
            # Exibe os pontos necessários para resgatar
            st.markdown(f"🪙 **{row['Pontos']} pontos**")
        
        with col3:
            # Exibe o tipo de recompensa (Pequena, Média, Grande)
            st.markdown(f"**Tipo**: {row['Tipo']}")

        with col4:
            # Exibe se a recompensa está desbloqueada ou não
            st.markdown(f"**Desbloqueada**: {'Sim' if row['Desbloqueada'] else 'Não'}")
        
        with col5:
            # Verifica se o usuário tem pontos suficientes para resgatar a recompensa
            if pontos_disponiveis >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos para liberar")
