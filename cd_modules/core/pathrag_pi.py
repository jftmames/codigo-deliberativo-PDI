# pathrag_pi.py

def recuperar_info_relacionada(pregunta):
    """
    Simulación de PathRAG: recuperación contextual basada en relaciones jurídicas.
    En un MVP real, esto se conecta con grafos legales u ontologías PI.
    """
    ejemplos_simulados = {
        "autor": "el autor es la persona física que crea una obra literaria, artística o científica",
        "marca": "una marca puede declararse nula si carece de carácter distintivo según el Reglamento 2017/1001",
        "registro": "el registro en la OEPM proporciona una presunción de validez de derechos",
    }
    for clave, valor in ejemplos_simulados.items():
        if clave.lower() in pregunta.lower():
            return valor
    return "el análisis debe hacerse conforme al principio de especialidad y la normativa aplicable"

