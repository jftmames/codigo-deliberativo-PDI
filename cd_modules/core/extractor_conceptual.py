# cd_modules/core/extractor_conceptual.py

def extraer_conceptos(texto):
    texto = texto.lower()
    conceptos_base = {
        "software": ["patente", "invención técnica", "automatización"],
        "ia": ["originalidad", "autoría automática", "algoritmo creativo"],
        "autor": ["derechos morales", "obra original", "reconocimiento"],
        "marca": ["registro", "distintivo comercial", "marca sonora"],
        "obra colectiva": ["editor", "responsabilidad compartida"],
        "españa": ["Ley 24/2015", "OEPM", "jurisdicción nacional"],
        "europea": ["directiva comunitaria", "armonización legal"],
        "patente": ["invención", "novedad", "actividad inventiva"],
        "voz": ["biometría", "tratamiento de datos"]
    }

    encontrados = []
    for clave, conceptos in conceptos_base.items():
        if clave in texto:
            encontrados.extend(conceptos)

    return list(set(encontrados))
