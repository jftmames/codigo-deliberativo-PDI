# cd_modules/core/inquiry_engine.py

class InquiryEngine:
    """
    Generador de árbol de indagación (Inquiry Tree).
    Simula la descomposición de una pregunta jurídica en subpreguntas relevantes.
    """
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        """
        Expande el nodo generando subpreguntas simuladas.
        """
        if depth >= self.max_depth:
            return {}
        hijos = {}
        for i in range(1, self.max_width + 1):
            subpregunta = f"Subpregunta {depth+1}.{i} sobre '{nodo}'"
            hijos[subpregunta] = self._expand(subpregunta, depth + 1)
        return hijos

    def generate(self):
        """
        Devuelve el árbol completo de preguntas y subpreguntas.
        """
        return {self.pregunta: self._expand(self.pregunta, 0)}

    def get_subquestions(self, nodo):
        """
        Devuelve las subpreguntas directas de un nodo.
        """
        return list(self._expand(nodo, 0).keys())
