# cd_modules/core/validador_epistemico.py

"""
Simulador de validación epistémica para el contexto generado en Derecho de Propiedad Intelectual.
Clasifica cada nodo legal en 'validada', 'parcial' o 'no validada' en función del tipo de fuente.
"""

def validar_contexto(nodo_legal):
    """
    Asigna una validación epistémica según el tipo de fuente del nodo recuperado.

    Args:
        nodo_legal (str): Etiqueta del nodo legal (ej. 'Artículo 5 LPI', 'Comentario doctrinal', etc.)

    Returns:
        str: Una de las siguientes categorías:
            - 'validada': si hay norma o sentencia clara
            - 'parcial': si hay solo doctrina o interpretación
            - 'no validada': si es sugerencia o vacío legal
    """
    if nodo_legal.startswith("Artículo") or "Sentencia" in nodo_legal:
        return "validada"
    elif "Comentario" in nodo_legal or "Informe" in nodo_legal:
        return "parcial"
    else:
        return "no validada"

# Ejemplo de uso
if __name__ == "__main__":
    ejemplos = [
        "Artículo 5 LPI",
        "Sentencia TS 123/2020",
        "Comentario doctrinal sobre autoría",
        "Propuesta de reforma futura"
    ]
    for e in ejemplos:
        print(f"{e} -> {validar_contexto(e)}")
