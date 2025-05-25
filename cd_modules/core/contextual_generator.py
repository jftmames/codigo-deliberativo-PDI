# cd_modules/core/contextual_generator.py

from cd_modules.core.pathrag_pi import recuperar_nodo_relevante
from cd_modules.core.validador_epistemico import validar_contexto

def generar_contexto(subpregunta: str) -> dict:
    """
    Simula la generación de contexto jurídico para una subpregunta dada.
    Integra recuperación por PathRAG simulado y validación epistémica.
    """
    # Simula recuperación legal basada en el grafo PI
    contexto, fuente = recuperar_nodo_relevante(subpregunta)

    # Simula validación epistémica
    validacion = validar_contexto(contexto)

    return {
        "contexto": contexto,
        "fuente": fuente,
        "validacion": validacion
    }
