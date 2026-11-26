import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gradio as gr
from intenciones.dialogo import contexto_inicial, procesar_mensaje

def responder(pregunta, history, contexto):
    history = history or []
    pregunta = pregunta.strip()
    if not pregunta:
        return "", history, contexto, None
    respuesta, contexto, diagnostico = procesar_mensaje(pregunta, contexto)
    history = history + [
        {"role": "user", "content": pregunta},
        {"role": "assistant", "content": respuesta},
    ]
    return "", history, contexto, diagnostico

with gr.Blocks() as demo:
    DinoBot = gr.Chatbot()
    msg = gr.Textbox(label="Escribe tu pregunta")
    estado = gr.State(contexto_inicial())
    diagnostico = gr.JSON(label="Diagnóstico del clasificador (modo de pruebas)")
    clear = gr.Button("Limpiar conversación")
    msg.submit(
        responder,
        inputs=[msg, DinoBot, estado],
        outputs=[msg, DinoBot, estado, diagnostico],
    )
    clear.click(
        lambda: ([], "", contexto_inicial(), None),
        outputs=[DinoBot, msg, estado, diagnostico],
        queue=False,
    )
