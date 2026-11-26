from .pruebaDeteccionDino import extraer_multiples_dinosaurios
from .deteccion_intencion import clasificar_intencion, respuestas

def contexto_inicial():
    return {"especies": [], "intencion_pendiente": None}

def procesar_mensaje(pregunta, contexto=None):
    """Devuelve respuesta, nuevo contexto y diagnostico sin depender de Gradio."""
    contexto = contexto or contexto_inicial()
    frase, detectadas = extraer_multiples_dinosaurios(pregunta)
    especies = detectadas or list(contexto["especies"])
    intencion = clasificar_intencion(frase)
    # Si el visitante solo responde con el nombre, recuperar la pregunta pendiente.
    if intencion is None and detectadas and not any(c.isalnum() for c in frase):
        intencion = contexto.get("intencion_pendiente")
    pendiente = None
    if intencion is None:
        respuesta = "¿Qué te gustaría saber sobre ese dinosaurio?" if especies else "No logré identificar el tema. ¿Qué te gustaría saber sobre los dinosaurios?"
    elif not especies:
        pendiente = intencion
        respuesta = "¿Sobre qué dinosaurio quieres preguntar?"
    else:
        respuesta = "\n".join(respuestas(intencion, d) for d in especies)
    diagnostico = {
        "texto_clasificado": frase,
        "intencion": intencion,
        "especies_detectadas": detectadas,
        "especies_contexto": especies,
    }
    return respuesta, {"especies": especies, "intencion_pendiente": pendiente}, diagnostico
