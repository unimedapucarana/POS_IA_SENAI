#TESTE NO COLAB: https://colab.research.google.com/drive/1tqtj68jgRKFHJe0P2qBZtKFsB51Ix3l5?usp=sharing

import pandas as pd
import numpy as np
import time
import warnings
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

warnings.filterwarnings("ignore")  # Silencia warnings

# ========================
# 1. Leitura do Dataset
# ========================
df = pd.read_csv("dataset.csv")  # Ajuste o nome se necessário
print("Dataset carregado com sucesso!")

# ========================
# 2. Pré-processamento
# ========================
X = df.iloc[:, 1:-1]
y = df.iloc[:, -1]

# Codifica o alvo se necessário
if y.dtype == 'object':
    y = LabelEncoder().fit_transform(y)

# Normalização
X = StandardScaler().fit_transform(X)

# Divisão em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=62)

# ========================
# 3. Definição de Modelos
# ========================
modelos = {
    "KNN": KNeighborsClassifier(n_jobs=-1),
    "Árvore de Decisão": DecisionTreeClassifier(random_state=42),
    "MLP": MLPClassifier(random_state=42, max_iter=1000),  # Usa CPU
    #"SVM": SVC(random_state=42),  # Usa GPU se tiver CUDA via CuPy/ONNX
    
    #"Random Forest": RandomForestClassifier(n_jobs=-1, random_state=42), # Modelo com os parametros no padrão

    "Random Forest": RandomForestClassifier(
                                                n_estimators=300,
                                                max_depth=30,
                                                min_samples_split=2,
                                                min_samples_leaf=1,
                                                max_features='sqrt',
                                                n_jobs=-1,
                                                random_state=42
                                            ), 

    "AdaBoost": AdaBoostClassifier(random_state=42),
    "Naive Bayes": GaussianNB()
}

# ========================
# 4. Treinamento e Avaliação
# ========================
resultados = []

for nome, modelo in modelos.items():
    print(f"Treinando: {nome}")
    tempo_inicio = time.time()
    modelo.fit(X_train, y_train)
    tempo_fim = time.time()
    tempo_treino = tempo_fim - tempo_inicio

    tempo_inicio = time.time()
    y_pred = modelo.predict(X_test)
    tempo_fim = time.time()
    tempo_teste = tempo_fim - tempo_inicio

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    precision = precision_score(y_test, y_pred, average='weighted')

    resultados.append({
        "Modelo": nome,
        "Acurácia": round(acc, 4),
        "F1-Score": round(f1, 4),
        "Revocação": round(recall, 4),
        "Precisão": round(precision, 4),
        "Tempo Treino (s)": round(tempo_treino, 2),
        "Tempo Teste (s)": round(tempo_teste, 2)
    })

# ========================
# 5. Resultados
# ========================
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

# Gráfico
df_resultados.set_index("Modelo")[["Acurácia", "F1-Score", "Revocação", "Precisão"]].plot(kind='bar', figsize=(12, 6))
plt.title("Comparação de Desempenho entre Modelos")
plt.ylabel("Pontuação")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico de tempo
df_resultados.set_index("Modelo")[["Tempo Treino (s)", "Tempo Teste (s)"]].plot(kind='barh', figsize=(12, 6), colormap='coolwarm')
plt.title("Tempo de Execução por Modelo")
plt.xlabel("Segundos")
plt.tight_layout()
plt.show()