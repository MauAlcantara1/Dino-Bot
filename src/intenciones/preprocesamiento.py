"""Limpieza conservadora para el clasificador de intenciones."""

import re
from unicodedata import normalize, combining

# No eliminar interrogativos, negaciones, preposiciones ni vocabulario tematico.
PALABRAS_COMUNES = frozenset(
    "dinosaurio dinosaurios dino dinos el la los las un una unos unas y".split()
)

def limpiar_texto(texto):
    normalizado = "".join(
        c for c in normalize("NFKD", texto.lower()) if not combining(c)
    )
    tokens = re.findall(r"[^\W_]+", normalizado)
    return " ".join(t for t in tokens if t not in PALABRAS_COMUNES)
