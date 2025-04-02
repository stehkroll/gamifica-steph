import streamlit as st
import pandas as pd
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from datetime import datetime
from components.personagem import montar_personagem

st.set_page_config(page_title="Gamificação da Rotina", layout="centered")

# Sidebar para mudar de página
pagina = st.sidebar.selectbox("Escolha uma página", ["Planejar o Dia", "Dia Atual"])

# Cria a memória para tarefas do dia e pontos, se ainda não existir
if "tarefas_do_dia" not in st.session_state:
    st.session_state.tarefas_do_dia = []

if "pontos_totais" not in st.session_state:
    st.session_state.pontos_totais = 0

# Página de planejamento
if pagina == "Planejar o Dia":
    st.title("📋 Planejar o Dia")

    # Carrega todas as tarefas disponíveis
    tarefas = pd.read_csv("data/tarefas.csv")
    opcoes = tarefas["Tarefa"].tolist()

    # Caixas para escolher as tarefas que vão aparecer no dia seguinte
    selecionadas = st.multiselect("Quais tarefas você quer fazer hoje?", opcoes)

    if st.button("✨ Programar Tarefas ✨"):
        st.session_state.tarefas_do_dia = selecionadas
        st.success("Tarefas programadas com sucesso! Agora vá para a página 'Dia Atual' 👇")

# Página principal: Dia Atual
elif pagina == "Dia Atual":
    # Configuração da página
    st.title("🌟 Gamificação da Rotina")

    # Data de hoje
    hoje = datetime.today().strftime('%Y-%m-%d')

    # Carrega tarefas do CSV
    tarefas = pd.read_csv("data/tarefas.csv")

    # Filtra só as tarefas que a pessoa planejou
    tarefas = tarefas[tarefas["Tarefa"].isin(st.session_state.tarefas_do_dia)]

    # Mostra painel de tarefas e retorna pontos do dia
    pontos = mostrar_painel_tarefas(tarefas)

    # Soma os pontos do dia no total
    st.session_state.pontos_totais += pontos

    # Botão para resetar as tarefas (mas manter os pontos!)
    st.markdown("---")
    if st.button("🔄 Resetar Dia"):
        st.session_state.tarefas_do_dia = []
        st.success("Tarefas resetadas! Volte à página 'Planejar o Dia' para começar de novo.")

    # Calcula nível, progresso e XP para o próximo nível
    nivel, xp_atual, xp_proximo_nivel, progresso = calcular_nivel(pontos)

    # Exibe informações de nível e progresso
    st.markdown("---")
    st.subheader(f"📊 Nível {nivel}")
    st.progress(progresso)
    st.caption(f"Você está a {xp_proximo_nivel - xp_atual} XP de alcançar o nível {nivel + 1}!")

    # Personalização do personagem
    st.markdown("---")
    st.subheader("🧍 Personalização do Personagem")

    # Escolhas do usuário
    olho_escolhido = st.selectbox("Escolha a cor dos olhos:", [
        "castanho", "azul", "verde", "roxo", "vermelho", "rosa"
    ])

    estilo_cabelo = st.selectbox("Escolha o estilo de cabelo:", [
        "sem_cabelo",
        "curto1", "curto2",
        "medio_liso", "medio_cacheado",
        "longo_liso", "longo_cacheado"
    ])

    cor_cabelo = st.selectbox("Escolha a cor do cabelo:", [
        "preto", "castanho", "vermelho", "rosa", "roxo",
        "azul", "verde", "loiro", "branco"
    ])

    # Combina estilo com cor
    cabelo_escolhido = f"{estilo_cabelo}_{cor_cabelo}"

    # Mostra personagem com as escolhas feitas
    montar_personagem(olho=olho_escolhido, cabelo=cabelo_escolhido)

    # Salva progresso diário
    progresso_df = pd.DataFrame([[hoje, pontos, nivel]], columns=["Data", "Pontos", "Nivel"])
    progresso_df.to_csv("data/progresso.csv", index=False)

    # Mostra painel de recompensas
    st.markdown("---")
    mostrar_painel_recompensas(pontos)
