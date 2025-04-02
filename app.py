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
    st.session_state.tarefas_do_dia = []

if "pontos_totais" not in st.session_state:
    st.session_state.pontos_totais = 0

# Página de planejamento
if pagina == "Planejar o Dia":
    st.title("📋 Planejar o Dia")

    # Carrega o CSV com todas as tarefas
    tarefas = pd.read_csv("data/tarefas.csv")

    # Lista onde vamos guardar tudo que foi selecionado
    tarefas_selecionadas = []

    # Agora vamos mostrar as tarefas separadas por categoria!
    for categoria, cor in cores_categorias.items():
        # 🔹 Título da categoria com fundinho colorido
        st.markdown(
            f"<div style='margin-top:20px'><span style='font-weight:bold; background-color:{cor}; padding:5px 15px; border-radius:10px; color:black'>{categoria}</span></div>",
            unsafe_allow_html=True
        )

        # 🔹 Filtra só as tarefas dessa categoria
        tarefas_da_categoria = tarefas[tarefas["Categoria"] == categoria]["Tarefa"].tolist()

        # 🔹 Caixinha de seleção (multiselect) pra essa categoria
        selecionadas = st.multiselect(
        "",
        tarefas_da_categoria,
        key=categoria
        )


        # 🔹 Mostrar as tarefas selecionadas com fundinho colorido (tipo TAG)
        for tarefa in selecionadas:
            st.markdown(
                f"<div style='display:inline-block; background-color:{cor}; color:black; padding:5px 10px; border-radius:10px; margin:5px 5px 10px 0;'>{tarefa}</div>",
                unsafe_allow_html=True
            )

        # 🔹 Adiciona as tarefas dessa categoria na lista geral
        tarefas_selecionadas.extend(selecionadas)

    # 🔹 Botão para salvar a programação do dia
    if st.button("✨ Programar Tarefas ✨"):
        st.session_state.tarefas_do_dia = tarefas_selecionadas
        st.success("Tarefas programadas com sucesso! Vá para a página 'Dia Atual'")


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
    # Filtra só as tarefas que a pessoa planejou
    tarefas = tarefas[tarefas["Tarefa"].isin(st.session_state.tarefas_do_dia)]

    # 🌈 Mostra cada tarefa com tag colorida da categoria
    st.subheader("Tarefas para hoje:")

    for _, linha in tarefas.iterrows():
        tarefa = linha["Tarefa"]
        categoria = linha["Categoria"]
        cor = cores_categorias.get(categoria, "#EEE")

        st.markdown(
            f"""
            <div style='padding:8px 12px; border-radius:10px; background-color:#f9f9f9; margin-bottom:10px; font-size:16px'>
                ✅ {tarefa}
                <span style='background-color:{cor}; color:black; padding:3px 10px; border-radius:8px; margin-left:10px; font-size:0.85em'>
                    {categoria}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

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
