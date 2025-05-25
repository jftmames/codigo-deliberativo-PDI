# pathrag_pi.py

def recuperar_nodo_relevante(subpregunta):
    """
    Simulación de recuperación PathRAG: devuelve un nodo PI relevante ficticio.
    """
    ejemplos = [
        "autoría", "derechos morales", "cesión de derechos", "registro", "plagio", "originalidad"
    ]
    import random
    return random.choice(ejemplos)
