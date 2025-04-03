import streamlit as st
import pandas as pd
import os
from datetime import datetime

from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from components.personagem import montar_personagem
from logic.niveis import calcular_nivel
from utils.salvar import salvar_pontos

st.set_page_config(page_title="Gamificação da Rotina", layout="centered")

# Cores para cada categoria
cores_categorias = {
    "Casa": "#E1B12C",
    "Estudos": "#7FDBD4",
    "Autocuidado": "#A2CFFF",
    "Trabalho": "#5BA67C",
    "Projetos": "#C89BE0",
}

# Garante que o arquivo de pontos exista
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/pontos_totais.csv"):
    pd.DataFrame([{"Pontos": 0}]).to_csv("data/pontos_totais.csv", index=False)

if "pontos_totais" not in st.session_state:
    pontos_df = pd.read_csv("data/pontos_totais.csv")
    st.session_state.pontos_totais = int(pontos_df["Pontos"].iloc[0])

# Verifica se há tarefas salvas
if "tarefas_do_dia" not in st.session_state:
    try:
        tarefas_salvas = pd.read_csv("data/tarefas_do_dia.csv")["Tarefa"].tolist()
    except FileNotFoundError:
        tarefas_salvas = []
    st.session_state.tarefas_do_dia = tarefas_salvas

pagina_inicial = "Dia Atual" if st.session_state.tarefas_do_dia else "Planejar o Dia"
pagina = st.sidebar.selectbox("Escolha uma página", ["Planejar o Dia", "Dia Atual"], index=0 if pagina_inicial == "Planejar o Dia" else 1)

tarefas_df = pd.read_csv("data/tarefas.csv")

if pagina == "Planejar o Dia":
    st.title("📋 Planejar o Dia")
    tarefas_selecionadas = []

    for categoria, cor in cores_categorias.items():
        st.markdown(f"<div style='margin-top:20px'><span style='font-weight:bold; background-color:{cor}; padding:5px 15px; border-radius:10px; color:black'>{categoria}</span></div>", unsafe_allow_html=True)
        opcoes = tarefas_df[tarefas_df["Categoria"] == categoria]["Tarefa"].tolist()
        selecionadas = st.multiselect("", opcoes, key=categoria)

        for tarefa in selecionadas:
            st.markdown(f"<div style='display:inline-block; background-color:{cor}; color:black; padding:5px 10px; border-radius:10px; margin:5px 5px 10px 0;'>{tarefa}</div>", unsafe_allow_html=True)

        tarefas_selecionadas.extend(selecionadas)

    if st.button("✨ Programar Tarefas ✨"):
        st.session_state.tarefas_do_dia = tarefas_selecionadas
        pd.DataFrame(tarefas_selecionadas, columns=["Tarefa"]).to_csv("data/tarefas_do_dia.csv", index=False)
        st.success("Tarefas programadas com sucesso! Vá para a página 'Dia Atual'")

elif pagina == "Dia Atual":
    st.title("🌟 Gamificação da Rotina")
    hoje = datetime.today().strftime('%Y-%m-%d')
    tarefas_ativas = tarefas_df[tarefas_df["Tarefa"].isin(st.session_state.tarefas_do_dia)]

    caminho_status = "data/status_tarefas.csv"
    try:
        status_df = pd.read_csv(caminho_status)
    except FileNotFoundError:
        status_df = pd.DataFrame(columns=["Tarefa", "Feita", "Data"])

    st.subheader("Tarefas para hoje:")
    pontos_ganhos_hoje = 0
    novos_status = []

    for _, linha in tarefas_ativas.iterrows():
        tarefa = linha["Tarefa"]
        categoria = linha["Categoria"]
        pontos_tarefa = linha["Pontos"]
        cor = cores_categorias.get(categoria, "#EEE")

        feita_antes = False
        anterior = status_df[status_df["Tarefa"] == tarefa]
        if not anterior.empty:
            feita_antes = bool(anterior["Feita"].values[0])

        feita_nova = st.checkbox(f"{tarefa}", value=feita_antes, key=f"checkbox_{tarefa}")

        st.markdown(f"<div style='margin-top:-10px; margin-bottom:10px;'><span style='background-color:{cor}; color:black; padding:3px 10px; border-radius:8px; font-size:0.85em'>{categoria}</span></div>", unsafe_allow_html=True)

        if feita_nova and not feita_antes:
            st.session_state.pontos_totais += pontos_tarefa
            pontos_ganhos_hoje += pontos_tarefa

        novos_status.append({"Tarefa": tarefa, "Feita": feita_nova, "Data": hoje})

    salvar_pontos()
    pd.DataFrame(novos_status).to_csv(caminho_status, index=False)

    # Exibe saldo total de pontos
    st.markdown(f"<div style='border: 2px solid #c89be0; padding: 15px; border-radius: 12px; background-color: #f2f2f2; text-align: center; font-size: 20px; margin-top: 20px; color: #000000'>💰 <b>Pontos:</b> {st.session_state.pontos_totais}</div>", unsafe_allow_html=True)

    if pontos_ganhos_hoje > 0:
        st.success(f"🚀 Você ganhou {pontos_ganhos_hoje} pontos hoje!")

    st.markdown("---")
    if st.button("🔄 Resetar Dia"):
        st.session_state.tarefas_do_dia = []
        pd.DataFrame(columns=["Tarefa"]).to_csv("data/tarefas_do_dia.csv", index=False)
        pd.DataFrame(columns=["Tarefa", "Feita", "Data"]).to_csv("data/status_tarefas.csv", index=False)
        st.success("Tarefas resetadas! Volte à página 'Planejar o Dia'")

    # Cálculo de XP e Nível com base nos pontos totais GANHOS, não saldo
    nivel, xp_atual, xp_proximo, progresso = calcular_nivel(st.session_state.pontos_totais)
    st.subheader(f"📊 Nível {nivel}")
    st.progress(progresso)
    st.caption(f"Você está a {xp_proximo - xp_atual} XP de alcançar o nível {nivel + 1}!")

    #st.markdown("---")
    #st.subheader("👽 Personalização do Personagem")
    #olho = st.selectbox("Escolha a cor dos olhos:", ["castanho", "azul", "verde", "roxo", "vermelho", "rosa"])
    #estilo = st.selectbox("Escolha o estilo de cabelo:", ["sem_cabelo", "curto1", "curto2", "medio_liso", "medio_cacheado", "longo_liso", "longo_cacheado"])
    #cor_cabelo = st.selectbox("Escolha a cor do cabelo:", ["preto", "castanho", "vermelho", "rosa", "roxo", "azul", "verde", "loiro", "branco"])
    #montar_personagem(olho=olho, cabelo=f"{estilo}_{cor_cabelo}")

    progresso_df = pd.DataFrame([[hoje, pontos_ganhos_hoje, nivel]], columns=["Data", "Pontos", "Nivel"])
    progresso_df.to_csv("data/progresso.csv", index=False)

    st.markdown("---")
    mostrar_painel_recompensas()
