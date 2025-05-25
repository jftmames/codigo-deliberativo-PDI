# cd_modules/core/inquiry_engine.py

SIMULATED_SUBTOPICS = [
    "definición legal",
    "jurisprudencia aplicable",
    "excepciones",
    "casos comparados",
    "autoría en obras colectivas",
    "derechos de menores de edad"
]

class InquiryEngine:
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

    def _expand(self, nodo, depth):
        if depth >= self.max_depth:
            return {}
        hijos = {}
        for i in range(self.max_width):
            tema = SIMULATED_SUBTOPICS[i % len(SIMULATED_SUBTOPICS)]
            subpregunta = f"{tema.capitalize()} relacionada con: {nodo}"
            hijos[subpregunta] = self._expand(subpregunta, depth + 1)
        return hijos

    def generate(self):
        return {self.pregunta: self._expand(self.pregunta, 0)}
