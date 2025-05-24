"""
Módulo ContextualGenerator
--------------------------
Genera una respuesta profesional a partir de una pregunta y fuentes relevantes.
Imita el razonamiento de un experto integrando evidencias recuperadas.
Perfecto para MVP, RAG académico y para integrar modelos generativos más adelante.
"""

class ContextualGenerator:
    def __init__(self):
        pass

    def generate(self, question, sources):
        """
        Recibe una pregunta y una lista de fuentes relevantes, y devuelve un texto explicativo.
        Si tienes LLM, puedes sustituir el return por una llamada a la IA real.
        """
        contexto = f"**Pregunta:** {question}\n\n"
        if sources:
            contexto += "Se han consultado las siguientes fuentes relevantes:\n"
            for src in sources:
                contexto += f"- {src}\n"
            contexto += "\n"
        contexto += (
            "Respuesta generada (demo):\n"
            "Según las fuentes seleccionadas y el análisis deliberativo, "
            "esta es la respuesta profesional simulada para la pregunta planteada."
        )
        return contexto
