from joblib import load
from random import choice


modelo = load("models/clasificador_intenciones.joblib")

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

    if intencion not in diccionario:
        return "Lo siento, no logre entender tu pregunta"

    opciones = diccionario[intencion].get(dinosaurio)

    if not opciones:
        return f"Lo siento aun no dispongo informacion sobre {dinosaurio}"

    return choice(opciones)


def detectar_intencion(frase, dinosaurios):

    vectorizar_frase = modelo.named_steps["tfidfvectorizer"]

    if vectorizar_frase.transform([frase]).nnz == 0:
        return None, dinosaurios
    
    intencion = modelo.predict([frase])[0]

    respuesta_final = respuestas(intencion, dinosaurios)
    return respuesta_final


print(detectar_intencion("Hola puedes hacerme un codigo para imprimir hola mundo en c", "Tyrannosaurus rex"))