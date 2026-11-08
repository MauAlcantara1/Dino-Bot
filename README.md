# DinoBot

DinoBot es un chatbot educativo en desarrollo para orientar a visitantes de una exposición sobre dinosaurios. El proyecto es académico y lo realiza un equipo de tres integrantes.

## Objetivo del proyecto

La versión final busca reconocer preguntas sobre un catálogo de 8–10 dinosaurios, identificar al menos 10 intenciones y responder con información revisada. También debe manejar preguntas de seguimiento, pedir aclaraciones cuando haya ambigüedad, responder cuando la consulta esté fuera del tema y permitir reiniciar la conversación.

Estos son los objetivos del proyecto; todavía no están implementados por completo.

## Estado actual

- El diccionario de especies contempla 8 dinosaurios: Tyrannosaurus rex, Triceratops, Stegosaurus, Brachiosaurus, Ankylosaurus, Velociraptor, Spinosaurus y Parasaurolophus.
- `data/prueba.xlsx`, hoja `Ejemplos`, contiene 40 ejemplos de prueba: 20 de `consultar_alimentacion` y 20 de `consultar_tamano`. Es un conjunto inicial, no el dataset final.
- El módulo de entrenamiento usa TF-IDF y LinearSVC. Divide los datos de ese Excel en entrenamiento y prueba con una partición aleatoria estratificada 80/20. Esa partición no sustituye al conjunto de prueba independiente que requiere la evaluación final.
- La interfaz Gradio permite escribir mensajes, muestra las especies que detecta el módulo experimental y permite limpiar el chat.
- La interfaz todavía no usa el clasificador de intenciones ni genera respuestas con datos paleontológicos. El historial se muestra, pero aún no se utiliza para entender preguntas de seguimiento.
- El detector devuelve `["Especie no detectada"]` cuando no encuentra una especie. Como la interfaz recibe una lista no vacía, puede mostrar ese texto como si fuera una especie detectada; este comportamiento está pendiente de corregirse.
- No se han publicado métricas finales ni un modelo entrenado guardado para cargar desde la interfaz.

## Estructura actual

```text
Dino-Bot/
├── data/
│   ├── diccionarios_especies.py
│   └── prueba.xlsx
├── documentacion/
│   └── prueba.txt
├── metricas/
│   └── prueba.txt
├── models/
│   ├── clasificador_intenciones.py
│   └── clasificador_intenciones.ipynb
├── src/
│   ├── intenciones/
│   │   ├── entrada_texto.py
│   │   └── pruebaDeteccionDino.py
│   ├── interfaz/
│   │   └── interfaz.py
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

El notebook se conserva como material experimental y no es necesario para iniciar la interfaz. Su ejecución queda pendiente de revisar.

## Instalación y ejecución de la interfaz

Ejecuta estos comandos desde la carpeta raíz del repositorio:

```bash
python -m venv .venv
```

Activa el entorno virtual:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS o Linux
source .venv/bin/activate
```

Instala las dependencias usadas por la interfaz y el prototipo del clasificador:

```bash
python -m pip install -r requirements.txt
```

Inicia la aplicación:

```bash
python src/main.py
```

Gradio mostrará en la terminal la dirección local para abrir el chatbot. La aplicación se inicia con `share=False`, por lo que no solicita crear un enlace público.

El archivo `requirements.txt` contiene las dependencias directas sin versiones fijadas. Antes de la entrega final, el equipo deberá probar y acordar versiones compatibles para reproducir el entorno.

## Datos de prueba

El archivo `data/prueba.xlsx` tiene una hoja llamada `Ejemplos` y estas columnas:

| Columna | Uso actual |
|---|---|
| `id` | Identificador del ejemplo |
| `texto` | Pregunta que recibe el clasificador |
| `intencion` | Etiqueta que el clasificador intenta predecir |
| `especie` | Dinosaurio relacionado con el ejemplo |
| `periodo` | Periodo geológico asociado |

El prototipo de entrenamiento usa solamente `texto` e `intencion`. El dataset final deberá ampliarse para cubrir las 10 intenciones y separarse en datos de entrenamiento/validación y un conjunto de prueba independiente. La meta planteada es contar con al menos 200 ejemplos de entrenamiento y 50 ejemplos de prueba.

## Módulos principales

| Ruta | Responsabilidad actual |
|---|---|
| `src/main.py` | Inicia la aplicación Gradio. |
| `src/interfaz/interfaz.py` | Presenta el chat, recibe preguntas y muestra el resultado de la detección de especies. |
| `src/intenciones/pruebaDeteccionDino.py` | Prueba la detección aproximada de nombres y alias de dinosaurios. |
| `src/intenciones/entrada_texto.py` | Archivo vacío, reservado para el procesamiento de la entrada. |
| `data/diccionarios_especies.py` | Contiene un diccionario de especies y alias. |
| `models/clasificador_intenciones.py` | Carga ejemplos desde Excel y entrena el prototipo TF-IDF + LinearSVC. |

## Pendientes para la versión final

- Acordar y documentar las 10 intenciones con su propósito, respuesta y ejemplos.
- Ampliar el dataset y documentar su etiquetado, revisión de duplicados y particiones.
- Comparar al menos dos clasificadores con el mismo protocolo y reportar accuracy, precisión, recall, F1 macro y matriz de confusión.
- Guardar el modelo elegido junto con su preprocesamiento e integrarlo en la aplicación.
- Crear el módulo de respuestas con información y fuentes verificables para las especies.
- Implementar y probar el contexto conversacional, las aclaraciones, las consultas fuera de dominio y el reinicio.
- Completar la documentación, las métricas y las instrucciones de instalación del equipo.

## Equipo

Proyecto académico de tres integrantes. Añadir los nombres y las responsabilidades acordadas por el equipo.
