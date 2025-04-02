import streamlit as st
import pandas as pd
import math
from datetime import datetime
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from components.personagem import montar_personagem

# Configuração da página
st.set_page_config(page_title="Gamificação da Rotina", layout="centered")
st.title("🌟 Gamificação da Rotina")

# Data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')

# Carrega tarefas do CSV
tarefas = pd.read_csv("data/tarefas.csv")

# Função para calcular pontos perdidos e ganhos
def calcular_pontos(tarefas_selecionadas):
    pontos_totais = 0
    for tarefa, prioridade, pontos in tarefas_selecionadas:
        # 50% dos pontos da tarefa
        pontos_perdidos = math.ceil(pontos * 0.5)

        # Bonificação/penalização baseada na prioridade (como porcentagem)
        if prioridade == 3:
            pontos_perdidos += math.ceil(pontos * 0.10)  # +10% dos pontos da tarefa
        elif prioridade == 2:
            pontos_perdidos += math.ceil(pontos * 0.06)  # +6% dos pontos da tarefa
        elif prioridade == 1:
            pontos_perdidos += math.ceil(pontos * 0.03)  # +3% dos pontos da tarefa

        # Adiciona a penalização ao total de pontos
        pontos_totais += pontos_perdidos
    
    return pontos_totais

# Função para o planejamento do dia
def planejar_o_dia():
    # Filtragem por categoria
    categorias = tarefas['Categoria'].unique()
    categoria_selecionada = st.selectbox("Escolha a categoria", categorias)

    # Exibir tarefas da categoria selecionada
    tarefas_filtradas = tarefas[tarefas['Categoria'] == categoria_selecionada]
    tarefas_selecionadas = []

    # Interface para escolher tarefas e definir prioridade
    st.markdown("### Planejando o Dia")

    for i, tarefa in tarefas_filtradas.iterrows():
        tarefa_escolhida = st.checkbox(tarefa['Tarefa'], key=f"tarefa_{i}")
        prioridade = st.slider(f"Prioridade de {tarefa['Tarefa']} (Deixe em branco se não escolher)", 0, 3, 0, key=f"prioridade_{i}")
        
        if tarefa_escolhida:
            tarefas_selecionadas.append((tarefa['Tarefa'], prioridade, tarefa['Pontos']))

    # Mostrar tarefas selecionadas
    st.markdown("### Tarefas Selecionadas para o Dia")
    for tarefa, prioridade, pontos in tarefas_selecionadas:
        prioridade_texto = "Sem Prioridade" if prioridade == 0 else f"Prioridade: {prioridade} estrela(s)"
        st.markdown(f"- {tarefa} ({prioridade_texto})")

    return tarefas_selecionadas

# Planejamento do dia
tarefas_selecionadas = planejar_o_dia()

# Botão para resetar tarefas e perder pontos
if st.button("Resetar Tarefas"):
    pontos_perdidos = calcular_pontos(tarefas_selecionadas)
    st.warning(f"Você perdeu {pontos_perdidos} pontos pelas tarefas não feitas!")

# Exibe informações de nível e progresso
pontos = mostrar_painel_tarefas(tarefas)
nivel, xp_atual, xp_proximo_nivel, progresso = calcular_nivel(pontos)
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
mostrar_painel_recompensas(pontos)
