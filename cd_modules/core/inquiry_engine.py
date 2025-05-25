# cd_modules/core/inquiry_engine.py

from cd_modules.core.extractor_conceptual import extraer_conceptos

class InquiryEngine:
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        if depth >= self.max_depth:
            return {}

        conceptos = extraer_conceptos(nodo)

        if conceptos:
            subpreguntas = [f"¿Qué implica el concepto de '{c}' en este contexto?" for c in conceptos]
        else:
            subpreguntas = [
                f"¿Qué dice la legislación sobre '{nodo}'?",
                f"¿Existe jurisprudencia relevante sobre '{nodo}'?",
                f"¿Qué interpretación doctrinal existe sobre '{nodo}'?",
                f"¿Cómo afecta la legislación europea a '{nodo}'?"
            ]

        hijos = {}
        for i, sub in enumerate(subpreguntas[:self.max_width]):
            hijos[sub] = self._expand(sub, depth + 1)
        return hijos

    def generate(self):
        return {self.pregunta: self._expand(self.pregunta, 0)}
