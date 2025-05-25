def generar_subpreguntas_desde_ontologia(nodo_texto):
    rutas = buscar_conceptos_relacionados(nodo_texto)
    subpreguntas = []

    for ruta in rutas:
        conceptos = buscar_nodo(ruta)
        if isinstance(conceptos, list):
            for concepto in conceptos:
                subpreguntas.append(f"¿Cómo se aplica el concepto de '{concepto}' en relación con '{nodo_texto}'?")
        elif isinstance(conceptos, dict):
            for clave in conceptos:
                subpreguntas.append(f"¿Qué papel cumple '{clave}' dentro de '{nodo_texto}'?")
    
    return subpreguntas[:4] if subpreguntas else [f"¿Qué regulación afecta a '{nodo_texto}'?"]
