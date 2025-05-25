# cd_modules/core/contextual_generator.py

"""
Generador de contexto jurídico simulado para preguntas del árbol de razonamiento.
Integra recuperación desde PathRAG PI y validación epistémica.
"""

from cd_modules.core.pathrag_pi import recuperar_nodo_relevante
from cd_modules.core.validador_epistemico import validar_contexto

def generar_contexto(subpregunta):
    """
    Genera un contexto jurídico simulado para una subpregunta,
    recuperando un nodo relevante (PathRAG) y validando epistemológicamente.

    Args:
        subpregunta (str): Pregunta jurídica concreta del árbol

    Returns:
        dict: {
            "contexto": str,
            "fuente": str,
            "validacion": str  # "validada", "parcial", "no validada"
        }
    """
    nodo = recuperar_nodo_relevante(subpregunta)

    # Simulamos la generación de contexto explicativo (mock)
    contexto = f"Según el {nodo}, la cuestión de '{subpregunta}' está regulada en ese marco jurídico. \
Debe interpretarse conforme a la jurisprudencia y doctrina aplicable."

    # Aplicamos validador epistémico simulado
    validacion = validar_contexto(nodo)

    return {
        "contexto": contexto,
        "fuente": nodo,
        "validacion": validacion
    }

# Ejemplo de uso
if __name__ == "__main__":
    subp = "¿Quién puede ser autor de una obra?"
    resultado = generar_contexto(subp)
    for k, v in resultado.items():
        print(f"{k}: {v}")
