from pathlib import Path
from joblib import load
from random import choice
from .preprocesamiento import limpiar_texto

BASE_DIR = Path(__file__).resolve().parents[2]
modelo = load(BASE_DIR / "models" / "clasificador_intenciones.joblib")

def clasificar_intencion(frase):
    """Clasificar independientemente de la especie y de las respuestas disponibles."""
    frase = limpiar_texto(frase)
    if not frase or modelo.named_steps["tfidfvectorizer"].transform([frase]).nnz == 0:
        return None
    return str(modelo.predict([frase])[0])

def respuestas(intencion, dinosaurio):
    diccionario = {
        "consultar_alimentacion": {
            "Tyrannosaurus rex": [
                "El Tyrannosaurus rex era carnívoro: se alimentaba de carne.",
                "En cuanto a su alimentación, el Tyrannosaurus rex comía carne.",
                "La dieta del Tyrannosaurus rex era carnívora.",
            ],
            "Triceratops": [
                "El Triceratops era herbívoro: se alimentaba de plantas.",
                "En cuanto a su alimentación, el Triceratops comía plantas.",
                "La dieta del Triceratops era herbívora.",
            ],
        },
        "consultar_tamano": {
            "Tyrannosaurus rex": [
                "El Tyrannosaurus rex medía aproximadamente 12 metros de largo.",
                "Se estima que el Tyrannosaurus rex alcanzaba unos 12 metros de longitud.",
                "En longitud, el Tyrannosaurus rex rondaba los 12 metros.",
            ],
            "Triceratops": [
                "El Triceratops medía aproximadamente 9 metros de largo.",
                "Se estima que el Triceratops alcanzaba unos 9 metros de longitud.",
                "En longitud, el Triceratops rondaba los 9 metros.",
            ],
        },
    }
    opciones = diccionario.get(intencion, {}).get(dinosaurio)
    if not opciones:
        return f"Reconocí el tema de tu pregunta, pero todavía no tengo una respuesta implementada para {dinosaurio} ({intencion})."
    return choice(opciones)

def detectar_intencion(frase, dinosaurios):
    intencion = clasificar_intencion(frase)
    if intencion is None:
        return "Lo siento, no logré entender tu pregunta."
    if not dinosaurios:
        return "¿Sobre qué dinosaurio quieres preguntar?"
    return "\n".join(respuestas(intencion, d) for d in dinosaurios)
