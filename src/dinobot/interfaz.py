import gradio as gr
from pruebaDeteccionDino import extraer_multiples_dinosaurios


def responder(pregunta, history):
    history = history or []
    pregunta = pregunta.strip()

    if not pregunta:
        return "", history

    # La pregunta viene directamente del Textbox como texto.
    dinosaurios = extraer_multiples_dinosaurios(pregunta)

    if dinosaurios:
        respuesta = "Dinosaurios detectados: " + ", ".join(dinosaurios)
    else:
        respuesta = "No encontre dinosaurios en tu pregunta."

    history = history + [
        {"role": "user", "content": pregunta},
        {"role": "assistant", "content": respuesta}
    ]

    return "", history


with gr.Blocks() as demo:
    DinoBot = gr.Chatbot()
    msg = gr.Textbox(label="Escribe tu pregunta")
    clear = gr.Button("Limpiar conversación")

    msg.submit(
        responder,
        inputs=[msg, DinoBot],
        outputs=[msg, DinoBot]
    )

    clear.click(
        lambda: ([], ""),
        outputs=[DinoBot, msg],
        queue=False
    )


if __name__ == "__main__":
    demo.launch(share=False)