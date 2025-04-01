# app.py

import streamlit as st
import pandas as pd
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from datetime import datetime

st.set_page_config(page_title="Gamifica Steph", layout="centered")
st.title("🌟 Gamificação da Rotina")

# 📅 Data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')
st.session_state['data_hoje'] = hoje

# 📋 Carrega tarefas do CSV
tarefas = pd.read_csv("data/tarefas.csv")

# ✅ Mostra painel de tarefas + retorna pontos do dia
pontos = mostrar_painel_tarefas(tarefas)

# 📈 Calcula XP, nível e progresso
nivel, progresso, xp_prox = calcular_nivel(pontos)

st.markdown("---")
st.subheader(f"📊 Nível {nivel}")
st.progress(progresso)
st.caption(f"Você está {round(progresso * 100)}% do caminho até o nível {nivel + 1}!")

# 💾 Salva progresso diário (opcional)
progresso_df = pd.DataFrame([[hoje, pontos, nivel]], columns=["Data", "Pontos", "Nivel"])
progresso_df.to_csv("data/progresso.csv", index=False)

# 🎁 Mostra painel de recompensas
st.markdown("---")
mostrar_painel_recompensas(pontos)
