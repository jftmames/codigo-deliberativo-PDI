from typing import List

class InquiryEngine:
    """
    Genera una jerarquía de preguntas a partir de una cuestión inicial.
    Implementación provisional: sólo devuelve la raíz.
    """
    def __init__(self, root_question: str):
        self.root = root_question

    def generate(self) -> List[str]:
        return [self.root]
