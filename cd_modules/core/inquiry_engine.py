"""
Módulo InquiryEngine
--------------------
Genera un árbol deliberativo de preguntas y subpreguntas a partir de una pregunta raíz.
Permite configurar la profundidad (niveles de subpreguntas) y la anchura (cuántas subpreguntas por nivel).
Ideal para visualizar y estructurar el razonamiento epistémico.
"""

class InquiryEngine:
    def __init__(self, question, depth=2, width=3):
        """
        Inicializa el motor con la pregunta raíz, la profundidad y la anchura.
        """
        self.question = question
        self.depth = depth
        self.width = width

    def generate(self):
        """
        Devuelve una lista de diccionarios, cada uno representando un nivel del árbol:
            [{pregunta_padre: [subpregunta1, subpregunta2, ...]}, ...]
        Por defecto, las subpreguntas son generadas automáticamente para demo/MVP.
        """
        tree = []
        current_parents = [self.question]
        for nivel in range(self.depth):
            capa = {}
            next_parents = []
            for parent in current_parents:
                hijos = [
                    f"{parent} [subpregunta {i+1}]" for i in range(self.width)
                ]
                capa[parent] = hijos
                next_parents.extend(hijos)
            tree.append(capa)
            current_parents = next_parents
        return tree
