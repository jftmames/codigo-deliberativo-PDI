from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# ───────────────────────────  Prompt de sistema  ────────────────────────────
SYSTEM_PROMPT = """\
Eres un asistente jurídico experto.
A partir de una PREGUNTA RAÍZ, genera {width} sub-preguntas claras y directas
que, si se responden, permitan resolver la pregunta padre.
Devuelve únicamente la lista, cada elemento en una línea y sin numeración extra.\
"""

@dataclass
class InquiryEngine:
    """
    Genera una jerarquía de preguntas (árbol) con anchura y profundidad
    configurables.
    """
    root_question: str
    depth: int = 2                 # niveles de recursión
    width: int = 3                 # sub-preguntas por nivel
    model_name: str = "gpt-4o-mini"

    # ────────────────────  helpers internos  ────────────────────
    def _llm(self):
        return ChatOpenAI(model=self.model_name, temperature=0.2)

    # ───────────────────–  API pública  ─────────────────────────
    def generate(self) -> List[Dict[str, List[str]]]:
        """
        Devuelve una lista de capas; cada capa es
        {pregunta_padre: [hijo1, hijo2, …]}.
        """
        prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", "{q}")]
        )

        queue: List[str] = [self.root_question]
        tree: List[Dict[str, List[str]]] = []

        for _ in range(self.depth):
            if not queue:
                break

            parent = queue.pop(0)
            response = self._llm().invoke(
                prompt.format_messages(q=parent, width=self.width)
            )

            children = [
                line.strip("-• ").rstrip(".")
                for line in response.content.split("\n") if line.strip()
            ][: self.width]

            tree.append({parent: children})
            queue.extend(children)

        if not tree:
            tree.append({self.root_question: []})
        return tree
