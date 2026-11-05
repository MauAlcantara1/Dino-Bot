import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC

def intenciones(ruta_excel):
        
    intenciones = pd.read_excel(ruta_excel, sheet_name="Ejemplos")

    x = intenciones["texto"].str.strip()
    y = intenciones["intencion"].str.strip()

    return x, y

def entrenar_clasificador(ruta_excel):
    X, y = intenciones(ruta_excel)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=0,
        stratify=y,
    )

    modelo = make_pipeline(TfidfVectorizer(), LinearSVC())
    modelo.fit(X_train, y_train)

    exactitud = modelo.score(X_test, y_test)

    print(f"Preguntas de entrenamiento: {len(X_train)}")
    print(f"Preguntas de prueba: {len(X_test)}")
    print(f"Exactitud en prueba: {exactitud:.1%}")

    return modelo