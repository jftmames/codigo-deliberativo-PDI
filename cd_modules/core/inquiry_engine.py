# inquiry_engine.py

class InquiryEngine:
    """
    Generador de árbol de indagación simulada para preguntas jurídicas.
    """
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        if depth >= self.max_depth:
            return {}
        hijos = {}
        for i in range(1, self.max_width + 1):
            subpregunta = f"Subpregunta {depth+1}.{i} sobre '{nodo}'"
            hijos[subpregunta] = self._expand(subpregunta, depth + 1)
        return hijos

    def generate(self):
        return {self.pregunta: self._expand(self.pregunta, 0)}
