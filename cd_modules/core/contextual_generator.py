from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

RAG_PROMPT = """
Eres un asistente jurídico. A partir de la pregunta y los extractos relevantes, 
genera una respuesta clara, breve y profesional usando solo la información dada. 
No inventes nada fuera del contexto. 
———
Pregunta: {question}
Fuentes:
{sources}
———
Respuesta profesional:
"""

class ContextualGenerator:
    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.0)
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT)

    def generate(self, question: str, sources: list[str]) -> str:
        formatted_sources = "\n".join(f"- {src}" for src in sources)
        msg = self.prompt.format_messages(
            question=question,
            sources=formatted_sources
        )
        result = self.llm.invoke(msg)
        return result.content.strip()
