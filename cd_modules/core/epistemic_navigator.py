from typing import List

class EpistemicNavigator:
    """
    Stub: devuelve cadenas de texto simulando resultados.
    Sustituye FAISS temporalmente.
    """
    def search(self, question: str, k: int = 3) -> List[str]:
        return [f"(stub) Resultado {i+1} para '{question}'" for i in range(k)]
