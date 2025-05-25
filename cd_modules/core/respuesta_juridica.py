# cd_modules/core/respuesta_juridica.py

def generar_respuesta(subpregunta, nodo_padre, nivel):
    if "autoría" in nodo_padre.lower():
        return (
            f"En el contexto de la propiedad intelectual, la autoría se refiere "
            f"a la titularidad moral e intelectual de una obra. "
            f"La legislación española reconoce este derecho a las personas físicas "
            f"que han creado obras originales. Véase Ley de Propiedad Intelectual, Art. 5."
        )

    if "software" in nodo_padre.lower() or "patentabilidad" in subpregunta.lower():
        return (
            f"El software, por sí solo, no es patentable en España. "
            f"Sin embargo, si está vinculado a una solución técnica concreta, puede ser protegible. "
            f"Esto se recoge en la Ley 24/2015 de Patentes, Art. 4.5, y en la jurisprudencia del TJUE."
        )

    if "marca" in nodo_padre.lower():
        return (
            f"Las marcas son signos que distinguen productos o servicios en el mercado. "
            f"Las marcas sonoras, aunque menos comunes, pueden registrarse si son susceptibles de representación gráfica. "
            f"Consulta la Ley 17/2001, de Marcas, Art. 4."
        )

    # Default genérico
    return (
        f"Esta cuestión se aborda dentro del marco legal de la propiedad intelectual. "
        f"Dependiendo del caso específico, pueden aplicarse normas nacionales o europeas, así como doctrina consolidada."
    )
