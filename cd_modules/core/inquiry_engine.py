# cd_modules/core/inquiry_engine.py

class InquiryEngine:
    """
    Generador de árbol de indagación (Inquiry Tree).
    A partir de una pregunta inicial, genera subpreguntas y estructura de razonamiento.
    """
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        """
        Expande el nodo generando subpreguntas simuladas (mockup).
        Retorna un diccionario {subpregunta: hijos}
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
        Devuelve un árbol de diccionarios con la estructura de preguntas/subpreguntas.
        Ejemplo de salida:
        {
            '¿Qué es una marca?': {
                'Subpregunta 1.1 sobre ...': {},
                'Subpregunta 1.2 sobre ...': {}
            }
        }
        """
        return {self.pregunta: self._expand(self.pregunta, 0)}

    def get_subquestions(self, nodo):
        """
        Devuelve lista de subpreguntas directas de un nodo.
        """
        return list(self._expand(nodo, 0).keys())

# Ejemplo de uso (no se ejecuta al importar)
if __name__ == "__main__":
    ie = InquiryEngine("¿Qué es una marca comunitaria?", max_depth=2, max_width=2)
    tree = ie.generate()
    print(tree)
