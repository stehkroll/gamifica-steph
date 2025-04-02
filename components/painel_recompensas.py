import streamlit as st
import pandas as pd

def mostrar_painel_recompensas(pontos_disponiveis):
    st.subheader("🎁 Recompensas")

    # Carregar recompensas do CSV
    recompensas = pd.read_csv("data/recompensas.csv")
    
    # Garantir que não existam espaços extras nas colunas
    recompensas.columns = recompensas.columns.str.strip()

    # Exibir as colunas para depuração

    # Loop através das recompensas
    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            # Exibir o emoji junto ao nome da recompensa, com um tamanho de fonte menor
            st.markdown(f"<h3 style='font-size: 18px; margin: 0;'>{row['Nome']} {row['Emoji']}</h3>", unsafe_allow_html=True)  # Nome + Emoji
        with col2:
            # Exibir pontos e a opção de resgatar
            if pontos_disponiveis >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - pontos_disponiveis} pontos para liberar")
