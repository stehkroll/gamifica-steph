import streamlit as st
import pandas as pd
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from datetime import datetime
from components.personagem import montar_personagem

# Configuração da página
st.set_page_config(page_title="Gamificação da Rotina", layout="centered")
st.title("🌟 Gamificação da Rotina")

# Data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')

# Carrega tarefas do CSV
tarefas = pd.read_csv("data/tarefas.csv")

# Mostra painel de tarefas e retorna pontos do dia
pontos = mostrar_painel_tarefas(tarefas)

# Calcula nível, progresso e XP para o próximo nível
nivel, xp_atual, xp_proximo_nivel, progresso = calcular_nivel(pontos)

# Exibe informações de nível e progresso
st.markdown("---")
st.subheader(f"📊 Nível {nivel}")
st.progress(progresso)
st.caption(f"Você está a {xp_proximo_nivel - xp_atual} XP de alcançar o nível {nivel + 1}!")

# Personagem
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

# Aqui chamamos o painel de recompensas
mostrar_painel_recompensas(pontos)

# Para verificar o que está acontecendo com o CSV
recompensas = pd.read_csv("data/recompensas.csv")
st.write("Colunas carregadas no CSV:", recompensas.columns.tolist())  # Exibe as colunas carregadas
