from rapidfuzz import process, fuzz, utils
import re

# Diccionario simplificado: solo nombres base y alias completamente distintos
entidades_base = [
    "Tyrannosaurus rex", "t-rex", "tiranosaurio",
    "Triceratops", "tres cuernos",
    "Stegosaurus", "estegosaurio",
    "Brachiosaurus", "braquiosaurio", "cuello largo",
    "Ankylosaurus", "anquilosaurio",
    "Velociraptor", "raptor",
    "Spinosaurus", "espinosaurio",
    "Parasaurolophus", "parasaurolofo"
]

# 2. Mapeamos TODAS las variaciones al nombre oficial de tu dataset
mapa_alias = {
    "t-rex": "Tyrannosaurus rex",
    "tiranosaurio": "Tyrannosaurus rex",
    "tres cuernos": "Triceratops",
    "estegosaurio": "Stegosaurus",
    "braquiosaurio": "Brachiosaurus",
    "cuello largo": "Brachiosaurus",
    "anquilosaurio": "Ankylosaurus",
    "raptor": "Velociraptor",
    "espinosaurio": "Spinosaurus",
    "parasaurolofo": "Parasaurolophus"
}

def extraer_multiples_dinosaurios(oracion):
    coincidencias = process.extract(
        oracion, 
        entidades_base, 
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
        limit=None
    )

    dinosaurios_encontrados = set()
    palabras_a_eliminar = set()

    for entidad, puntaje, _ in coincidencias:
        if puntaje >= 60:
            nombre_oficial = mapa_alias.get(entidad, entidad)
            dinosaurios_encontrados.add(nombre_oficial)

            for token in utils.default_process(entidad).split():
                palabras_a_eliminar.add(token)

    if not dinosaurios_encontrados:
        return oracion.strip(), []

    palabras_restantes = []
    for palabra in oracion.split():
        # Separamos en sub-tokens por si la palabra tiene guiones (ej. "t-rex" -> ["t", "rex"])
        sub_tokens = utils.default_process(palabra).split()
        
        if sub_tokens:
            es_dinosaurio = True
            for sub in sub_tokens:
                coincide = False
                for token_dino in palabras_a_eliminar:
                    if len(sub) <= 2:
                        if sub == token_dino:
                            coincide = True
                            break
                    elif fuzz.ratio(sub, token_dino) >= 80:
                        coincide = True
                        break
                # Si al menos un pedazo no es dinosaurio, conservamos la palabra
                if not coincide:
                    es_dinosaurio = False
                    break
        else:
            es_dinosaurio = False

        if not es_dinosaurio:
            palabras_restantes.append(palabra)

    frase_limpia = re.sub(r'\s+', ' ', " ".join(palabras_restantes)).strip()

    print("Frase detectada:", frase_limpia)
    print("Dinos detectados:", list(dinosaurios_encontrados))
    return frase_limpia, list(dinosaurios_encontrados)

# Prueba
#extraer_multiples_dinosaurios("Que comen los cuello largo y los t-rex y los tres cuernos")
# Salida esperada: ['Tyrannosaurus rex', 'Triceratops']