# cd_modules/core/consultor_ontologia.py

from .ontologia_pi import ONTOLOGIA_PI

def buscar_nodo(ruta):
    """
    Permite navegar por la ontología mediante una ruta tipo:
    ["Propiedad Intelectual", "Derechos de autor", "Obras"]
    """
    nodo = ONTOLOGIA_PI
    for paso in ruta:
        if paso in nodo:
            nodo = nodo[paso]
        else:
            return None
    return nodo

def buscar_conceptos_relacionados(termino):
    """
    Busca el término en el grafo y devuelve las rutas donde aparece.
    """
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
    """
    A partir de un término, genera subpreguntas relevantes basadas en su posición
    dentro de la ontología de propiedad intelectual.
    """
    rutas = buscar_conceptos_relacionados(nodo_texto)
    subpreguntas = []

    for ruta in rutas:
        conceptos = buscar_nodo(ruta)
        if isinstance(conceptos, list):
            for concepto in conceptos:
                subpreguntas.append(f"¿Cómo se aplica el concepto de '{concepto}' en relación con '{nodo_texto}'?")
        elif isinstance(conceptos, dict):
            for clave in conceptos:
                subpreguntas.append(f"¿Qué papel cumple '{clave}' dentro de '{nodo_texto}'?")
    
    return subpreguntas[:4] if subpreguntas else [f"¿Qué regulación afecta a '{nodo_texto}'?"]
