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

# ⏩ Verifica se o dia já está planejado
try:
    tarefas_salvas = pd.read_csv("data/tarefas_do_dia.csv")["Tarefa"].tolist()
except FileNotFoundError:
    tarefas_salvas = []

pagina_inicial = "Dia Atual" if tarefas_salvas else "Planejar o Dia"
pagina = st.sidebar.selectbox("Escolha uma página", ["Planejar o Dia", "Dia Atual"], index=0 if pagina_inicial == "Planejar o Dia" else 1)

# Session State
if "tarefas_do_dia" not in st.session_state:
    st.session_state.tarefas_do_dia = tarefas_salvas

if "pontos_totais" not in st.session_state:
    st.session_state.pontos_totais = 0

# 📅 Planejamento
if pagina == "Planejar o Dia":
    st.title("📋 Planejar o Dia")
    tarefas = pd.read_csv("data/tarefas.csv")
    tarefas_selecionadas = []

    for categoria, cor in cores_categorias.items():
        st.markdown(
            f"<div style='margin-top:20px'><span style='font-weight:bold; background-color:{cor}; padding:5px 15px; border-radius:10px; color:black'>{categoria}</span></div>",
            unsafe_allow_html=True
        )

        tarefas_da_categoria = tarefas[tarefas["Categoria"] == categoria]["Tarefa"].tolist()

        selecionadas = st.multiselect(
            "",
            tarefas_da_categoria,
            key=categoria
        )

        for tarefa in selecionadas:
            st.markdown(
                f"<div style='display:inline-block; background-color:{cor}; color:black; padding:5px 10px; border-radius:10px; margin:5px 5px 10px 0;'>{tarefa}</div>",
                unsafe_allow_html=True
            )

        tarefas_selecionadas.extend(selecionadas)

    if st.button("✨ Programar Tarefas ✨"):
        st.session_state.tarefas_do_dia = tarefas_selecionadas
        df_salvar = pd.DataFrame(tarefas_selecionadas, columns=["Tarefa"])
        df_salvar.to_csv("data/tarefas_do_dia.csv", index=False)
        st.success("Tarefas programadas com sucesso! Vá para a página 'Dia Atual'")

# 📆 Dia Atual
elif pagina == "Dia Atual":
    st.title("🌟 Gamificação da Rotina")
    hoje = datetime.today().strftime('%Y-%m-%d')
    tarefas = pd.read_csv("data/tarefas.csv")

    try:
        tarefas_do_dia_df = pd.read_csv("data/tarefas_do_dia.csv")
        tarefas_do_dia = tarefas_do_dia_df["Tarefa"].tolist()
    except FileNotFoundError:
        tarefas_do_dia = []

    tarefas = tarefas[tarefas["Tarefa"].isin(tarefas_do_dia)]

    st.subheader("Tarefas para hoje:")

    pontos = 0
    for _, linha in tarefas.iterrows():
        tarefa = linha["Tarefa"]
        categoria = linha["Categoria"]
        pontos_tarefa = linha["Pontos"]
        cor = cores_categorias.get(categoria, "#EEE")

        concluida = st.checkbox(
            f
