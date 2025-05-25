# File: cd_modules/core/informe_tracker.py
"""
Generador de reportes en Markdown a partir de pasos de razonamiento.
"""

def generar_markdown_reporte(pregunta: str, pasos: list) -> str:
    """
    Construye un informe en Markdown con los pasos de razonamiento.

    :param pregunta: Texto de la pregunta original.
    :param pasos: Lista de dicts con información de cada paso, puede incluir:
                   - 'nivel': nivel de indentación (int)
                   - 'descripcion': texto descriptivo del paso
                   - 'message': mensaje alternativo
    :return: String con el informe en formato Markdown.
    """
    md_lines = [f"# Informe de Trazabilidad para: {pregunta}\n"]
    for paso in pasos:
        nivel = paso.get("nivel", 0)
        indent = "  " * nivel
        # Priorizar 'descripcion', si no existe, usar 'message', o representar el dict completo
        contenido = paso.get("descripcion") or paso.get("message") or str(paso)
        md_lines.append(f"{indent}- {contenido}")
    # Unir líneas con salto de línea
    return "\n".join(md_lines)
