# cd_modules/core/pathrag_pi.py

"""
Módulo simulado de PathRAG para Derecho de la Propiedad Intelectual (PI).
Simula la recuperación semántica guiada por grafo (Path Retrieval-Augmented Generation).
"""

def recuperar_nodo_relevante(pregunta):
    """
    Simula la recuperación de un nodo relevante desde una ontología PI.
    Esta función devolverá una etiqueta jurídica que representa el nodo más relacionado.

    Args:
        pregunta (str): Subpregunta del árbol de razonamiento

    Returns:
        str: Nodo jurídico simulado (ej. artículo, doctrina, tratado)
    """
    pregunta = pregunta.lower()

    if "autor" in pregunta:
        return "Artículo 5 LPI – Presunción de autoría"
    elif "obra colectiva" in pregunta:
        return "Artículo 7 LPI – Obra colectiva"
    elif "obra derivada" in pregunta:
        return "Artículo 11 LPI – Obra derivada"
    elif "registro" in pregunta or "inscripción" in pregunta:
        return "Registro OEPM – Procedimiento administrativo"
    elif "duración" in pregunta or "plazo" in pregunta:
        return "Artículo 26 LPI – Duración de los derechos"
    elif "moral" in pregunta:
        return "Artículo 14 LPI – Derechos morales"
    elif "reproducción" in pregunta:
        return "Artículo 18 LPI – Derecho de reproducción"
    elif "transformación" in pregunta:
        return "Artículo 21 LPI – Derecho de transformación"
    elif "sentencia" in pregunta or "jurisprudencia" in pregunta:
        return "STS 294/2021 – Caso cita y parodia"
    elif "marca comunitaria" in pregunta:
        return "Reglamento (UE) 2017/1001 – Marca de la UE"
    else:
        return "Concepto general en Ontología PI"

# Ejemplo de uso directo
if __name__ == "__main__":
    preguntas = [
        "¿Quién puede ser autor de una obra?",
        "¿Qué derechos tiene una obra derivada?",
        "¿Cuál es la duración de los derechos?",
        "¿Qué regula la jurisprudencia sobre la cita?",
    ]
    for p in preguntas:
        print(f"{p} → {recuperar_nodo_relevante(p)}")
