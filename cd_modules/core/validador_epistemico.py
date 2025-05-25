# cd_modules/core/validador_epistemico.py
from .consultor_ontologia import generar_subpreguntas_desde_ontologia

import re

def validar_contexto(nodo, contexto):
    contexto = contexto.lower()

    # Validación legal explícita
    if re.search(r"ley\s+\d+/\d+", contexto) and "art" in contexto:
        return "validada"
    
    # Jurisprudencia reconocible
    if "sentencia" in contexto and ("tjue" in contexto or "ts" in contexto or "audiencia" in contexto):
        return "parcial"

    # Doctrina o fuentes no oficiales
    if "doctrina" in contexto or "según" in contexto:
        return "parcial"

    # Ninguna fuente válida
    return "no validada"
