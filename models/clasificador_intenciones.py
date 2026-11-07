import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_EXCEL = BASE_DIR / "data" / "prueba.xlsx"
RUTA_MODELO = Path(__file__).resolve().with_name(
    "clasificador_intenciones.joblib"
)

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
    modelo.fit(X, y)
    joblib.dump(modelo, RUTA_MODELO)
    return modelo

if __name__ == "__main__":
    entrenar_clasificador(RUTA_EXCEL)