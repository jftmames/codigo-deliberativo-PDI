# contextual_generator.py

from cd_modules.core.pathrag_pi import recuperar_nodo_relevante
from cd_modules.core.validador_epistemico import validar_contexto

def generar_contexto(subpregunta):
    """
    Simula la generación de contexto, fuente y validación epistémica.
    """
    nodo_relevante = recuperar_nodo_relevante(subpregunta)
    contexto = f"Análisis jurídico generado para: {subpregunta}. Basado en el nodo '{nodo_relevante}'."
    fuente = f"Simulación basada en jurisprudencia relacionada con '{nodo_relevante}'."
    validacion = validar_contexto(contexto)

    return {
        "contexto": contexto,
        "fuente": fuente,
        "validacion": validacion
    }
