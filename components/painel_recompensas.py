import streamlit as st
import pandas as pd
from app import salvar_pontos  # você precisa ter essa função no app.py

def mostrar_painel_recompensas(_):  # o _ é só um nome simbólico, já que não usamos
    st.subheader("🎁 Recompensas")

    # Carrega recompensas do CSV
    recompensas = pd.read_csv("data/recompensas.csv")
    recompensas.columns = recompensas.columns.str.strip()

    # Loop por recompensa
    for i, row in recompensas.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h3 style='font-size: 18px; margin: 0;'>{row['Nome']} {row['Emoji']}</h3>", unsafe_allow_html=True)

        with col2:
            # Verifica se tem pontos suficientes
            if st.session_state.pontos_totais >= row["Pontos"]:
                if st.button(f"✨ Resgatar", key=f"resgatar_{i}"):
                    # 🧮 SUBTRAI os pontos
                    st.session_state.pontos_totais -= row["Pontos"]

                    # 💾 SALVA os pontos no CSV
                    salvar_pontos()

                    # 🎉 Mostra mensagem de sucesso
                    st.success(f"🎉 Recompensa desbloqueada: {row['Nome']}")
            else:
                st.info(f"🔒 Faltam {row['Pontos'] - st.session_state.pontos_totais} pontos para liberar")
