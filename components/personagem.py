import streamlit as st
from PIL import Image
import os

# Caminho base das imagens
BASE_PATH = "assets/personagem"

def carregar_imagem(caminho):
    return Image.open(caminho)

def montar_personagem(olho="castanho", cabelo="curto1_preto"):
    st.subheader("🧍 Seu Personagem")

    try:
        corpo = carregar_imagem(os.path.join(BASE_PATH, "corpo_base.png"))
        roupa = carregar_imagem(os.path.join(BASE_PATH, "roupa_base.png"))
        olhos = carregar_imagem(os.path.join(BASE_PATH, "olhos", f"{olho}.png"))
        cabelo_img = carregar_imagem(os.path.join(BASE_PATH, "cabelo", f"{cabelo}.png"))

        corpo.paste(olhos, (0, 0), olhos)
        corpo.paste(cabelo_img, (0, 0), cabelo_img)
        corpo.paste(roupa, (0, 0), roupa)

        st.image(corpo, use_column_width=True)

    except FileNotFoundError as e:
        st.warning(f"❌ Imagem não encontrada: {e}")
        st.info("Você precisa adicionar as imagens na pasta assets/personagem")
