import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from intenciones.dialogo import contexto_inicial, procesar_mensaje
from intenciones.pruebaDeteccionDino import extraer_multiples_dinosaurios
from intenciones.preprocesamiento import limpiar_texto
from intenciones.deteccion_intencion import clasificar_intencion

class TestDialogo(unittest.TestCase):
    def test_dataset(self):
        datos = pd.read_excel(ROOT / "data" / "prueba.xlsx", sheet_name="Ejemplos")
        for fila in datos.itertuples():
            with self.subTest(texto=fila.texto):
                _, _, debug = procesar_mensaje(fila.texto, contexto_inicial())
                self.assertEqual(debug["intencion"], fila.intencion)
                self.assertEqual(debug["especies_detectadas"], [])

    def test_limpieza(self):
        self.assertEqual(limpiar_texto("que comian los dinosaurios y"), "que comian")
        self.assertEqual(limpiar_texto("¿Dónde no vivía el dinosaurio?"), "donde no vivia")
        self.assertEqual(limpiar_texto("¿Cuánto pesaba?"), "cuanto pesaba")
        self.assertEqual(limpiar_texto("¿En qué época vivió?"), "en que epoca vivio")
        self.assertIsNone(clasificar_intencion("los dinosaurios y"))
        self.assertEqual(clasificar_intencion("que comian los dinosaurios y"), "consultar_alimentacion")

    def test_limpieza_en_dialogo(self):
        _, _, debug = procesar_mensaje("que comian los dinosaurios t-rex y velociraptor")
        self.assertEqual(debug["texto_clasificado"], "que comian")
        self.assertEqual(debug["intencion"], "consultar_alimentacion")
        self.assertEqual(debug["especies_detectadas"], ["Tyrannosaurus rex", "Velociraptor"])

    def test_detector(self):
        self.assertEqual(extraer_multiples_dinosaurios("¿Qué comía el T-rex?"), ("¿Qué comía?", ["Tyrannosaurus rex"]))
        self.assertEqual(extraer_multiples_dinosaurios("¿Qué comía?"), ("¿Qué comía?", []))

    def test_contexto(self):
        respuesta, estado, debug = procesar_mensaje("¿Qué comía el T-rex?")
        self.assertEqual(debug["intencion"], "consultar_alimentacion")
        self.assertIn("car", respuesta.lower())
        _, estado, debug = procesar_mensaje("¿Cuánto medía?", estado)
        self.assertEqual(debug["intencion"], "consultar_tamano")
        self.assertEqual(debug["especies_contexto"], ["Tyrannosaurus rex"])
        _, _, debug = procesar_mensaje("¿En qué época vivió?", estado)
        self.assertEqual(debug["intencion"], "consultar_epoca")
        _, _, debug = procesar_mensaje("¿Cuánto medía?", contexto_inicial())
        self.assertEqual(debug["especies_contexto"], [])

    def test_aclaracion(self):
        _, estado, debug = procesar_mensaje("¿Qué comía?")
        self.assertEqual(debug["intencion"], "consultar_alimentacion")
        respuesta, _, debug = procesar_mensaje("T-rex", estado)
        self.assertEqual(debug["intencion"], "consultar_alimentacion")
        self.assertIn("car", respuesta.lower())

if __name__ == "__main__":
    unittest.main()
