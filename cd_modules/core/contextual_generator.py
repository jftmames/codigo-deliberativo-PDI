# cd_modules/core/contextual_generator.py

class ContextualGenerator:
    """
    Simula la generación de contexto legal para una pregunta/subpregunta.
    En futuro, conecta con LLM, PathRAG o bases legales reales.
    """
    def __init__(self, pregunta):
        self.pregunta = pregunta

    def get_context(self):
        # Aquí simulas una respuesta bien fundamentada.
        ejemplos = [
            f"Según el artículo 4 de la Directiva 2015/2436/UE, {self.pregunta} implica analizar los requisitos de distintividad.",
            f"La jurisprudencia reciente del TJUE (asunto C-25/19) aborda {self.pregunta} y los criterios de registrabilidad.",
            f"El BOE recoge en su última actualización la doctrina sobre {self.pregunta}.",
            f"La OEPM señala que {self.pregunta} debe interpretarse conforme a la finalidad protectora de la PI."
        ]
        
        # Rotar ejemplo para variar un poco
        idx = abs(hash(self.pregunta)) % len(ejemplos)
        return ejemplos[idx]
