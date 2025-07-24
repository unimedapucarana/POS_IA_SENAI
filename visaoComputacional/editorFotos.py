import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(layout="wide")
st.title("🖼️ Editor de Fotos com Streamlit")
st.markdown("---")
st.caption("Desenvolvido por Gleysson Bettin | Unimed Apucarana – Turma: SESCOOP 2025")


# Funções de transformação
def aplicar_rotacao(img, angulo):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angulo, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def aplicar_escala(img, escala):
    return cv2.resize(img, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)

def aplicar_cisalhamento(img, shear_x=0.0, shear_y=0.0):
    h, w = img.shape[:2]
    M = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
    return cv2.warpAffine(img, M, (w, h))

def ajustar_brilho_contraste(img, brilho=0, contraste=1.0):
    img = img.astype(np.float32)
    img = img * contraste + brilho
    return np.clip(img, 0, 255).astype(np.uint8)

def transformar_intensidade(img, tipo="linear"):
    img_float = img.astype(np.float32) / 255.0
    if tipo == "log":
        img_transf = np.log1p(img_float) / np.log(2)
    elif tipo == "gama":
        gamma = st.sidebar.slider("Gama", 0.1, 5.0, 1.0)
        img_transf = np.power(img_float, gamma)
    else:
        img_transf = img_float
    return np.clip(img_transf * 255, 0, 255).astype(np.uint8)

def aplicar_negativo(img):
    return 255 - img

# Interface de imagem
opcao = st.sidebar.radio("Escolha uma opção de entrada:", ["Upload de Imagem", "Captura via Webcam"])

imagem = None
if opcao == "Upload de Imagem":
    arquivo = st.file_uploader("Envie sua imagem", type=["jpg", "jpeg", "png"])
    if arquivo:
        imagem = Image.open(arquivo)
        imagem = np.array(imagem)
elif opcao == "Captura via Webcam":
    imagem_bytes = st.camera_input("Capture uma imagem")
    if imagem_bytes:
        imagem = Image.open(imagem_bytes)
        imagem = np.array(imagem)

# Se imagem carregada:
if imagem is not None:
    st.image(imagem, caption="Imagem Original", use_container_width=True)

    st.sidebar.subheader("Ajustes Geométricos")
    angulo = st.sidebar.slider("Rotação (graus)", -180, 180, 0)
    escala = st.sidebar.slider("Escala", 0.1, 3.0, 1.0)
    shear_x = st.sidebar.slider("Cisalhamento X", -1.0, 1.0, 0.0)
    shear_y = st.sidebar.slider("Cisalhamento Y", -1.0, 1.0, 0.0)

    st.sidebar.subheader("Ajustes de Intensidade")
    brilho = st.sidebar.slider("Brilho", -100, 100, 0)
    contraste = st.sidebar.slider("Contraste", 0.5, 3.0, 1.0)
    tipo_transformacao = st.sidebar.selectbox("Transformação Personalizada", ["Nenhuma", "log", "gama"])

    aplicar_filtro_negativo = st.sidebar.checkbox("Aplicar Filtro Negativo")

    # Aplicações das transformações
    imagem_proc = imagem.copy()

    imagem_proc = aplicar_rotacao(imagem_proc, angulo)
    imagem_proc = aplicar_escala(imagem_proc, escala)
    imagem_proc = aplicar_cisalhamento(imagem_proc, shear_x, shear_y)
    imagem_proc = ajustar_brilho_contraste(imagem_proc, brilho, contraste)
    imagem_proc = transformar_intensidade(imagem_proc, tipo_transformacao)
    
    if aplicar_filtro_negativo:
        imagem_proc = aplicar_negativo(imagem_proc)

    st.image(imagem_proc, caption="Imagem Editada", use_container_width=True)

    # Download da imagem
    img_pil = Image.fromarray(imagem_proc)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("📥 Baixar Imagem Editada", data=byte_im, file_name="imagem_editada.png", mime="image/png")

else:
    st.info("Envie ou capture uma imagem para começar.")


