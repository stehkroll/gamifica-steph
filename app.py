import streamlit as st
import pandas as pd
from components.painel_tarefas import mostrar_painel_tarefas
from components.painel_recompensas import mostrar_painel_recompensas
from logic.niveis import calcular_nivel
from datetime import datetime
from components.personagem import montar_personagem
from utils.salvar import salvar_pontos


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
    try:
        pontos_df = pd.read_csv("data/pontos_totais.csv")
        st.session_state.pontos_totais = int(pontos_df["Pontos"].iloc[0])
    except:
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
    # Caminho para salvar o status das tarefas
    caminho_status = "data/status_tarefas.csv"

# Tenta carregar o status anterior
    try:
        status_df = pd.read_csv(caminho_status)
    except FileNotFoundError:
        status_df = pd.DataFrame(columns=["Tarefa", "Feita", "Data"])
    
        st.subheader("Tarefas para hoje:")

        pontos = 0
        pontos = 0
        novos_status = []

    pontos = 0
    novos_status = []

    for _, linha in tarefas.iterrows():

        tarefa = linha["Tarefa"]
        categoria = linha["Categoria"]
        pontos_tarefa = linha["Pontos"]
        cor = cores_categorias.get(categoria, "#EEE")

        # Verifica se a tarefa está marcada como feita anteriormente
        status_anterior = status_df[status_df["Tarefa"] == tarefa]
        feita = False
        if not status_anterior.empty:
            feita = bool(status_anterior["Feita"].values[0])

        # Checkbox para marcar como feita
        feita_nova = st.checkbox(f"{tarefa}", value=feita, key=f"checkbox_{tarefa}")

        # Exibe categoria como tag colorida
        st.markdown(
            f"""
            <div style='margin-top:-10px; margin-bottom:10px;'>
                <span style='background-color:{cor}; color:black; padding:3px 10px; border-radius:8px; font-size:0.85em'>
                    {categoria}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Soma os pontos se marcada
        if feita_nova:
            pontos += pontos_tarefa

        # Atualiza lista para salvar
        novos_status.append({
            "Tarefa": tarefa,
            "Feita": feita_nova,
            "Data": hoje
        })

    # Salva o status atualizado das tarefas
    status_df_atualizado = pd.DataFrame(novos_status)
    status_df_atualizado.to_csv("data/status_tarefas.csv", index=False)

    st.session_state.pontos_totais += pontos
    salvar_pontos()

    # Exibe total acumulado de pontos
    st.markdown(
        f"""
        <div style='border: 2px solid #c89be0; padding: 15px; border-radius: 12px; background-color: #f2f2f2; text-align: center; font-size: 20px; margin-top: 20px; color: #000000'>
            💰 <b>Pontos:</b> {st.session_state.pontos_totais}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.button("🔄 Resetar Dia"):
        st.session_state.tarefas_do_dia = []
        pd.DataFrame(columns=["Tarefa"]).to_csv("data/tarefas_do_dia.csv", index=False)
        st.success("Tarefas resetadas! Volte à página 'Planejar o Dia' para começar de novo.")

    nivel, xp_atual, xp_proximo_nivel, progresso = calcular_nivel(pontos)

    st.markdown("---")
    st.subheader(f"📊 Nível {nivel}")
    st.progress(progresso)
    st.caption(f"Você está a {xp_proximo_nivel - xp_atual} XP de alcançar o nível {nivel + 1}!")

    st.markdown("---")
    st.subheader("🧍 Personalização do Personagem")

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

    cabelo_escolhido = f"{estilo_cabelo}_{cor_cabelo}"
    montar_personagem(olho=olho_escolhido, cabelo=cabelo_escolhido)

    progresso_df = pd.DataFrame([[hoje, pontos, nivel]], columns=["Data", "Pontos", "Nivel"])
    progresso_df.to_csv("data/progresso.csv", index=False)

    st.markdown("---")
    mostrar_painel_recompensas(st.session_state.pontos_totais)



