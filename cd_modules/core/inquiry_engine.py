# cd_modules/core/inquiry_engine.py

class InquiryEngine:
    """
    Genera un árbol de razonamiento a partir de una pregunta raíz.
    Puede ampliarse para usar LLM o un grafo real en el futuro.
    """
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        """
        Expande recursivamente el árbol generando subpreguntas (mockup).
        """
        if depth >= self.max_depth:
            return {}
        hijos = {}
        for i in range(1, self.max_width + 1):
            sub = f"Subpregunta {depth+1}.{i} sobre '{nodo}'"
            hijos[sub] = self._expand(sub, depth + 1)
        return hijos

    def generate(self):
        """
        Devuelve el árbol de razonamiento en formato dict anidado.
        """
        return {self.pregunta: self._expand(self.pregunta, 0)}
