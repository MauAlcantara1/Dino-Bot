# DinoBot

Chatbot educativo que funcionará como guía de una exposición de museo sobre dinosaurios. El equipo delimitará un catálogo de 8–10 especies y entrenará un clasificador supervisado para reconocer al menos 10 intenciones.

## Objetivo

Interpretar preguntas escritas sobre las especies incluidas en el catálogo, mantener el contexto de una conversación breve y responder con información revisada. Cuando la pregunta sea ambigua, el sistema pedirá una aclaración; si queda fuera del tema, explicará el alcance de DinoBot.

## Alcance inicial

- Dominio: guía virtual de una exposición de museo sobre dinosaurios.
- Catálogo: 8–10 especies seleccionadas por el equipo; la lista y las fuentes se documentarán en `docs/dominio.md`.
- Clasificación: mínimo 10 intenciones distintas entrenadas con ejemplos etiquetados por el equipo.
- Datos: mínimo 200 ejemplos de entrenamiento y un conjunto de prueba independiente con al menos 50 ejemplos.
- Modelos por comparar: Multinomial Naive Bayes y Linear SVM, con TF-IDF como representación inicial propuesta.
- Conversación: contexto para preguntas de seguimiento, aclaraciones, respuesta fuera de dominio y reinicio.
- Interfaz prevista: Streamlit; la decisión final se confirmará en el equipo.

Las cifras, decisiones y modelos son requisitos o propuestas de trabajo; los resultados experimentales se añadirán cuando existan ejecuciones reproducibles.

## Estructura del repositorio

```text
DinoBot/
├── data/
│   └── templates/
│       ├── train_template.csv
│       └── test_template.csv
├── docs/
│   ├── conversaciones.md
│   └── dominio.md
├── models/                 # Modelos generados; no subir archivos grandes sin acordarlo
├── notebooks/              # Exploración y experimentación
├── reports/                # Métricas, tablas y reporte final
├── src/
│   └── dinobot/
│       ├── nlp/             # Normalización, TF-IDF y clasificación
│       ├── dialogue/        # Intenciones, contexto y respuestas
│       ├── knowledge/       # Catálogo de especies y fuentes
│       ├── interface/       # Interfaz Streamlit
│       └── evaluation/      # Métricas y evaluación final
├── tests/                  # Pruebas del sistema
├── .gitignore
└── README.md
```

## Dataset

Las plantillas de `data/templates/` contienen únicamente los encabezados. Copien y renombren para crear los archivos reales:

- `data/train.csv`: ejemplos de desarrollo y entrenamiento, mínimo 200 y al menos 20 por intención.
- `data/test.csv`: mínimo 50 frases nuevas, separadas y reservadas para la evaluación final.

Columnas: `id`, `texto`, `intencion`, `especie`. El modelo aprenderá la relación entre `texto` e `intencion`. `especie` sirve para consultar el catálogo y mantener el contexto; se deja vacía cuando el mensaje no nombra una especie.

No utilicen `test.csv` para seleccionar modelos, ajustar parámetros o modificar reglas. La comparación y selección se harán con validación dentro de los datos de desarrollo.

## Instalación y ejecución

Pendiente de completar al definir versiones y dependencias.

```bash
# Próximamente:
# python -m venv .venv
# pip install -r requirements.txt
# streamlit run src/dinobot/app.py
```

## Estado del proyecto

Fase actual: delimitar el dominio, acordar las intenciones, definir el formato de datos y preparar ejemplos de conversación. No hay métricas ni modelo final publicados todavía.

## Responsabilidad de los módulos

- `nlp/`: convierte el texto en características y permite entrenar o consultar los clasificadores.
- `dialogue/`: toma la intención predicha, conserva el contexto y decide si responde o pide aclaración.
- `knowledge/`: guarda fichas verificadas de las especies y sus fuentes.
- `interface/`: recibe mensajes y presenta las respuestas; el reinicio debe limpiar la conversación.
- `evaluation/`: calcula y presenta métricas sobre conjuntos de datos definidos para evaluación.
- `tests/`: espacio para comprobar componentes y flujos conversacionales cuando se implementen.

## Equipo

Proyecto académico de tres integrantes. Añadir aquí los nombres y responsabilidades acordadas.
