import re
from rapidfuzz import fuzz
from unicodedata import normalize, combining

# Alias explicitos; no comparamos la oracion completa con nombres.
ALIAS = {
    "Tyrannosaurus rex": ("tyrannosaurus rex", "tyrannosaurus", "t rex", "trex", "rex", "tiranosaurio rex", "tiranosaurio", "tyranosaurio"),
    "Triceratops": ("triceratops", "triceratop", "triseratops", "el de tres cuernos"),
    "Stegosaurus": ("stegosaurus", "estegosaurio", "estegosaurus", "el de las placas"),
    "Brachiosaurus": ("brachiosaurus", "braquiosaurio", "brachiosaurio", "el de cuello largo"),
    "Ankylosaurus": ("ankylosaurus", "anquilosaurio", "ankilosaurio", "el del mazo"),
    "Velociraptor": ("velociraptor", "velosiraptor", "raptor"),
    "Spinosaurus": ("spinosaurus", "espinosaurio", "spinosaurio"),
    "Parasaurolophus": ("parasaurolophus", "parasaurolofo", "parasaurolofus"),
}

def _normalizar(texto):
    return "".join(c for c in normalize("NFKD", texto.lower()) if not combining(c))

def extraer_multiples_dinosaurios(oracion):
    tokens = list(re.finditer(r"[^\W_]+", oracion, re.UNICODE))
    palabras = [_normalizar(t.group()) for t in tokens]
    aliases = sorted(
        [(a.split(), especie) for especie, nombres in ALIAS.items() for a in nombres],
        key=lambda x: -len(x[0]),
    )
    encontrados, intervalos = [], []
    i = 0
    while i < len(tokens):
        coincidencia = next(((a, e) for a, e in aliases if palabras[i:i+len(a)] == a), None)
        if coincidencia:
            a, especie = coincidencia
            n = len(a)
        else:
            # Solo errores de escritura de nombres largos; no borrar vocabulario comun.
            candidato = palabras[i]
            puntuaciones = sorted(
                [(max((fuzz.ratio(candidato, a[0]) for a, e in aliases
                       if e == especie and len(a) == 1 and len(a[0]) >= 7), default=0), especie)
                 for especie in ALIAS], reverse=True)
            if len(candidato) < 7 or puntuaciones[0][0] < 88 or puntuaciones[0][0] - puntuaciones[1][0] < 8:
                i += 1
                continue
            especie = puntuaciones[0][1]
            n = 1
        if especie not in encontrados:
            encontrados.append(especie)
        inicio = i
        if i > 0 and palabras[i-1] in {"el", "la", "los", "las", "un", "una"}:
            inicio -= 1
        intervalos.append((tokens[inicio].start(), tokens[i+n-1].end()))
        i += n
    if not encontrados:
        return oracion.strip(), []
    limpio = oracion
    for inicio, fin in reversed(intervalos):
        limpio = limpio[:inicio] + " " + limpio[fin:]
    limpio = re.sub(r"\s+", " ", limpio).strip()
    limpio = re.sub(r"\s+([?!.:,;])", r"\1", limpio)
    return limpio, encontrados

def actualizar_memoria(dinos_detectados, memoria):
    actuales, anteriores = memoria
    if dinos_detectados:
        return list(dinos_detectados), list(actuales)
    return list(actuales), list(anteriores)
