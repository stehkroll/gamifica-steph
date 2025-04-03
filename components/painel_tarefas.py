import streamlit as st
from datetime import datetime

def mostrar_painel_tarefas(df):
    st.subheader("✅ Tarefas do Dia")
    pontos = 0
    hoje = datetime.today().strftime('%Y-%m-%d')
    st.session_state['data_hoje'] = hoje

    for i, row in df.iterrows():
        checkbox_id = f"tarefa_{i}"
        if st.checkbox(f"{row['Tarefa']} ({row['Categoria']}) - {row['Pontos']} pts", key=checkbox_id):
            pontos += row["Pontos"]

    st.success(f"🎉 Você ganhou {pontos} pontos hoje!")
    return pontos
