# cd_modules/core/consultor_ontologia.py

from .ontologia_pi import ONTOLOGIA_PI

def buscar_nodo(ruta):
    nodo = ONTOLOGIA_PI
    for paso in ruta:
        if paso in nodo:
            nodo = nodo[paso]
        else:
            return None
    return nodo

def buscar_conceptos_relacionados(termino):
    rutas = []
    def recorrer(nodo, camino):
        if isinstance(nodo, dict):
            for k, v in nodo.items():
                recorrer(v, camino + [k])
        elif isinstance(nodo, list):
            if termino.lower() in [i.lower() for i in nodo]:
                rutas.append(camino)
    recorrer(ONTOLOGIA_PI, [])
    return rutas

def generar_subpreguntas_desde_ontologia(nodo_texto):
    rutas = buscar_conceptos_relacionados(nodo_texto)
    subpreguntas = []

    for ruta in rutas:
        conceptos = buscar_nodo(ruta)
        if isinstance(conceptos, list):
            for concepto in conceptos:
                subpreguntas.append(f"¿Cómo se aplica '{concepto}' en '{nodo_texto}'?")
        elif isinstance(conceptos, dict):
            for clave in conceptos:
                subpreguntas.append(f"¿Qué implica '{clave}' para '{nodo_texto}'?")

    if not subpreguntas:
        subpreguntas = [f"¿Qué regulación afecta directamente a '{nodo_texto}'?"]

    return subpreguntas
