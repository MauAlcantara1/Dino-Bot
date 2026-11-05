from pathlib import Path

from clasificador_intenciones import entrenar_clasificador


BASE_DIR = Path(__file__).resolve().parents[2]
RUTA_EXCEL = BASE_DIR / "data" / "templates" / "prueba.xlsx"


def main():
    entrenar_clasificador(RUTA_EXCEL)


if __name__ == "__main__":
    main()