# validador_epistemico.py

def validar_contexto(texto):
    """
    Simulación de validación epistémica:
    Devuelve una de tres categorías: 'validada', 'parcial', 'no validada'
    """
    import random
    return random.choices(
        ["validada", "parcial", "no validada"],
        weights=[0.5, 0.3, 0.2],
        k=1
    )[0]
