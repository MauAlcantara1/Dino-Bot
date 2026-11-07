from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[2]
RUTA_MODELO = BASE_DIR / "models" / "clasificador_intenciones.joblib"

modelo = joblib.load(RUTA_MODELO)


def identificar_intencion(texto):

    return modelo.predict([texto.strip()])[0]