import streamlit as st
import pandas as pd
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from datetime import datetime
from components.personagem import montar_personagem

st.set_page_config(page_title="Gamificação da Rotina", layout="centered")

cores_categorias = {
    "Casa": "#E1B12C",
    "Estudos": "#7FDBD4",
    "Autocuidado": "#A2CFFF",
    "Trabalho": "#5BA67C",
    "Projetos": "#C89BE0",
}

# Sidebar para mudar de página
pagina = st.sidebar.selectbox("Escolha uma página", ["Planejar o Dia", "Dia Atual"])

# Cria a memória para tarefas do dia e pontos, se ainda não existir
if "tarefas_do_dia" not in st.session_state:
    try:
        st.session_state.tarefas_do_dia = pd.read_csv("data/tarefas_do_dia.csv")["Tarefa"].tolist()
    except:
        st.session_state.tarefas_do_dia = []

if "pontos_totais" not in st.session_state:
    st.session_state.pontos_totais = 0

# Página de planejamento
if pagina == "Planejar o Dia":
    st.title("📋 Planejar o Dia")

    tarefas = pd.read_csv("data/tarefas.csv")
    tarefas_selecionadas = []

    for categoria, cor in cores_categorias.items():
        st.markdown(
            f"<div style='margin-top:20px'><span style='font-weight:bold; background-color:{cor}; padding:5px 15px; border-radius:10px; color:black'>{categoria}</span></div>",
            unsafe_allow_html=True
        )

        tarefas_da_categoria = tarefas[tarefas
