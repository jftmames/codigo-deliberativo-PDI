# cd_modules/core/validador_epistemico.py

def validador_epistemico(respuesta, contexto):
    # Chequeo sencillo de grounding: ¿los términos legales están en la respuesta?
    validaciones = {}
    for fragmento in contexto.split('\n'):
        clave = fragmento.split(":")[0].strip().lower()
        validaciones[clave] = clave in respuesta.lower()
    return validaciones
