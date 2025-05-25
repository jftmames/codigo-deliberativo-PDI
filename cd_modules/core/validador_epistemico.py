# validador_epistemico.py

def validar_contexto(contexto):
    """
    Simula una validación epistémica.
    Puede ampliarse con corpus, heurísticas o IA legal.
    """
    if "Reglamento" in contexto or "OEPM" in contexto:
        return "validada", "Reglamento 2017/1001"
    elif "persona física" in contexto:
        return "parcial", "Doctrina general sobre autoría"
    else:
        return "no validada", "Sin referencia legal clara"
