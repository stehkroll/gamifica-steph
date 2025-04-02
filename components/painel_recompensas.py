import streamlit as st
import pandas as pd
from utils.salvar import salvar_pontos

def mostrar_painel_recompensas(_):
    st.subheader("🎁 Recompensas")

    recompensas = pd.read_csv("data/recompensas.csv")
    recompensas.columns = recompensas.columns.str.strip()

    # Inicializa o controle de resgates se não existir
    if "resgates_feitos" not in st.session_state:
        st.session_state.resgates_feitos = []

    for i, row in recompensas.iterrows():
        nome_recompensa = row['Nome']
        pontos_necessarios = row['Pontos']
        chave_botao = f"resgatar_{i}_{len(st.session_state.resgates_feitos)}"  # chave única pra não repetir

        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(
                f"<h3 style='font-size: 18px; margin: 0;'>{nome_recompensa} {row['Emoji']}</h3>",
                unsafe_allow_html=True
            )

        with col2:
            if st.session_state.pontos_totais >= pontos_necessarios:
                if st.button(f"✨ Resgatar", key=chave_botao):
                    st.session_state.pontos_totais -= pontos_necessarios
                    st.session_state.resgates_feitos.append({
                        "nome": nome_recompensa,
                        "pontos": pontos_necessarios
                    })
                    salvar_pontos()
                    st.success(f"🎉 Recompensa desbloqueada: {nome_recompensa}")
            else:
                st.info(f"🔒 Faltam {pontos_necessarios - st.session_state.pontos_totais} pontos")
