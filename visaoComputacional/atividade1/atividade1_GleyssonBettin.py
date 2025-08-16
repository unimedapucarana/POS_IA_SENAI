# ===============================================================
# Atividade 1 - Disciplina: Visão Computacional
# Autor: Gleysson Bettin
# Descrição: Aplica técnicas de PDI em imagens satelitais NOAA GOES-East conforme roteiro da atividade.
# ===============================================================

import cv2
import numpy as np
import os

# === Caminhos das imagens ===
img1_path = "20251801050_GOES19-ABI-ssa-GEOCOLOR-1800x1080.jpg"
img2_path = "20251801150_GOES19-ABI-ssa-GEOCOLOR-1800x1080.jpg"
img3_path = "20251801250_GOES19-ABI-ssa-GEOCOLOR-1800x1080.jpg"

# === Pasta de saída ===
output_dir = "resultados"
os.makedirs(output_dir, exist_ok=True)

# === 1. Carregar imagens ===
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
img3 = cv2.imread(img3_path)

if img1 is None or img2 is None or img3 is None:
    raise FileNotFoundError("Erro: verifique os caminhos das imagens.")

# === 2. Converter para tons de cinza ===
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

cv2.imwrite(os.path.join(output_dir, "01_gray1.png"), gray1)
cv2.imwrite(os.path.join(output_dir, "01_gray2.png"), gray2)
cv2.imwrite(os.path.join(output_dir, "01_gray3.png"), gray3)

# === 3. Normalizar ===
norm1 = cv2.normalize(gray1, None, 0, 255, cv2.NORM_MINMAX)
norm2 = cv2.normalize(gray2, None, 0, 255, cv2.NORM_MINMAX)
norm3 = cv2.normalize(gray3, None, 0, 255, cv2.NORM_MINMAX)

cv2.imwrite(os.path.join(output_dir, "02_norm1.png"), norm1)
cv2.imwrite(os.path.join(output_dir, "02_norm2.png"), norm2)
cv2.imwrite(os.path.join(output_dir, "02_norm3.png"), norm3)

# === 4. Ajuste de brilho ===
brilho_val = 50
bright1 = cv2.convertScaleAbs(norm1, alpha=1, beta=brilho_val)
bright2 = cv2.convertScaleAbs(norm2, alpha=1, beta=brilho_val)
bright3 = cv2.convertScaleAbs(norm3, alpha=1, beta=brilho_val)

cv2.imwrite(os.path.join(output_dir, "03_bright1.png"), bright1)
cv2.imwrite(os.path.join(output_dir, "03_bright2.png"), bright2)
cv2.imwrite(os.path.join(output_dir, "03_bright3.png"), bright3)

# === 5. Limiarização ===
limiar = 127
_, thresh1 = cv2.threshold(bright1, limiar, 255, cv2.THRESH_BINARY)
_, thresh2 = cv2.threshold(bright2, limiar, 255, cv2.THRESH_BINARY)
_, thresh3 = cv2.threshold(bright3, limiar, 255, cv2.THRESH_BINARY)

cv2.imwrite(os.path.join(output_dir, "04_thresh1.png"), thresh1)
cv2.imwrite(os.path.join(output_dir, "04_thresh2.png"), thresh2)
cv2.imwrite(os.path.join(output_dir, "04_thresh3.png"), thresh3)

# === 6. Inversão ===
inv1 = cv2.bitwise_not(thresh1)
inv2 = cv2.bitwise_not(thresh2)
inv3 = cv2.bitwise_not(thresh3)

cv2.imwrite(os.path.join(output_dir, "05_inv1.png"), inv1)
cv2.imwrite(os.path.join(output_dir, "05_inv2.png"), inv2)
cv2.imwrite(os.path.join(output_dir, "05_inv3.png"), inv3)

# === 7. Operações Lógicas (pares) ===
# AND
and12 = cv2.bitwise_and(inv1, inv2)
and23 = cv2.bitwise_and(inv2, inv3)
and13 = cv2.bitwise_and(inv1, inv3)
cv2.imwrite(os.path.join(output_dir, "06_and12.png"), and12)
cv2.imwrite(os.path.join(output_dir, "06_and23.png"), and23)
cv2.imwrite(os.path.join(output_dir, "06_and13.png"), and13)

# OR
or12 = cv2.bitwise_or(inv1, inv2)
or23 = cv2.bitwise_or(inv2, inv3)
or13 = cv2.bitwise_or(inv1, inv3)
cv2.imwrite(os.path.join(output_dir, "07_or12.png"), or12)
cv2.imwrite(os.path.join(output_dir, "07_or23.png"), or23)
cv2.imwrite(os.path.join(output_dir, "07_or13.png"), or13)

# XOR
xor12 = cv2.bitwise_xor(inv1, inv2)
xor23 = cv2.bitwise_xor(inv2, inv3)
xor13 = cv2.bitwise_xor(inv1, inv3)
cv2.imwrite(os.path.join(output_dir, "08_xor12.png"), xor12)
cv2.imwrite(os.path.join(output_dir, "08_xor23.png"), xor23)
cv2.imwrite(os.path.join(output_dir, "08_xor13.png"), xor13)

# === 8. Subtração (pares) ===
sub12 = cv2.absdiff(gray1, gray2)
sub23 = cv2.absdiff(gray2, gray3)
sub13 = cv2.absdiff(gray1, gray3)

cv2.imwrite(os.path.join(output_dir, "09_sub12.png"), sub12)
cv2.imwrite(os.path.join(output_dir, "09_sub23.png"), sub23)
cv2.imwrite(os.path.join(output_dir, "09_sub13.png"), sub13)

# (Opcional) Empilhamento final para visualização
stack_horizontal = np.hstack([gray1, gray2, gray3])
cv2.imwrite(os.path.join(output_dir, "10_stack_horizontal.png"), stack_horizontal)

stack_vertical = np.vstack([and12, or12, xor12, sub12])
cv2.imwrite(os.path.join(output_dir, "11_stack_vertical.png"), stack_vertical)

print("Processamento concluído! Resultados salvos na pasta:", output_dir)
