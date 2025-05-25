# cd_modules/core/informe_tracker.py
from cd_modules.core.respuesta_juridica import generar_respuesta

def generar_markdown_reporte(pregunta_principal, tracker):
    md = f"# Informe de Razonamiento Jurídico\n\n"
    md += f"**Pregunta inicial:** {pregunta_principal}\n\n"
    md += "---\n"
    for paso in tracker:
    indent = "  " * paso["nivel"]
    md += f"{indent}- **Subpregunta:** {paso['subpregunta']}\n"
    md += f"{indent}  - Nodo padre: *{paso['nodo_padre']}*\n"
    if paso["ruta"]:
        rutas = [" → ".join(r) for r in paso["ruta"]]
        rutas_md = "\n".join([f"{indent}    - Ruta ontológica: `{r}`" for r in rutas])
        md += rutas_md + "\n"

    respuesta = generar_respuesta(paso["subpregunta"], paso["nodo_padre"], paso["nivel"])
    md += f"{indent}  - **Respuesta explicativa:** {respuesta}\n\n"

    