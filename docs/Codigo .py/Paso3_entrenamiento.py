"""
PFM: SISTEMA DE SCORING CREDITICIO BASADO EN HÁBITOS DIGITALES
Script: Entrenamiento y Selección de Modelos
"""
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def entrenar():
    """Compara modelos, guarda el ganador (scoring_model.pkl) y genera gráficos para los entregables."""
    X = pd.read_csv('data/X_processed.csv')
    y = pd.read_csv('data/y_labels.csv').values.ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

    modelos = {
        'RandomForest': RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        'XGBoost': XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)}

    mejor_acc, modelo_final = 0, None

    for nombre, clf in modelos.items():
        clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        print(f"{nombre} Precisión: {acc*100:.2f} %")
        if acc >= mejor_acc:
            mejor_acc, modelo_final = acc, clf

    #ENTREGABLES GRÁFICOS
    #1. Matriz de Confusión
    plt.figure(figsize=(7, 5))
    sns.heatmap(confusion_matrix(y_test, modelo_final.predict(X_test)), annot=True, fmt='d', cmap='Blues')
    plt.title(f'Matriz de Confusión - Accuracy: {mejor_acc:.2f}')
    plt.savefig('entregables/confusion_matrix.png')

    #2. Importancia de Variables    
    importancias = pd.Series(modelo_final.feature_importances_, index=X.columns).sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    importancias.plot(kind='bar', color='steelblue')
    plt.title('Importancia de Variables en el Score')
    plt.savefig('entregables/importancia_variables.png')

    #ARTEFACTO 2: Modelo
    joblib.dump(modelo_final, 'models/scoring_model.pkl')

if __name__ == "__main__":
    entrenar()