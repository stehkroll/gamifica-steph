import pandas as pd
import streamlit as st

def salvar_pontos():
    df_pontos = pd.DataFrame([{"Pontos": st.session_state.pontos_totais}])
    df_pontos.to_csv("data/pontos_totais.csv", index=False)
