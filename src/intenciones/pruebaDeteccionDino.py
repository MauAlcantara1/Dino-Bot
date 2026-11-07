from rapidfuzz import process, fuzz, utils

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
    # process.extract devuelve una lista de tuplas: [(entidad, puntaje, indice), ...]
    coincidencias = process.extract(
        oracion, 
        entidades_base, 
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
        limit=None # Nos aseguramos de que evalúe toda la lista
    )
    
    # Usamos un 'set' (conjunto) en lugar de una lista para evitar que 
    # se guarde el mismo dinosaurio dos veces.
    dinosaurios_encontrados = set()
    
    for entidad, puntaje, _ in coincidencias:
        if puntaje >= 60:
            # Traducimos la entidad encontrada a su nombre oficial
            nombre_oficial = mapa_alias.get(entidad, entidad)
            dinosaurios_encontrados.add(nombre_oficial)
            
    if dinosaurios_encontrados:
        return list(dinosaurios_encontrados) # Lo convertimos de vuelta a lista para usarlo
        
    return frase_limpia, dinosaurios_encontrados

# Prueba
 
# Salida esperada: ['Tyrannosaurus rex', 'Triceratops']