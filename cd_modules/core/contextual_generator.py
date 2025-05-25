# cd_modules/core/contextual_generator.py

from langchain_openai import ChatOpenAI

class ContextualGenerator:
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name

    def generar_contexto(self, pregunta, contexto):
        llm = ChatOpenAI(model=self.model_name, temperature=0.2, api_key=self.api_key)
        prompt = (
            f"Eres un abogado especialista en propiedad intelectual. Responde únicamente usando el siguiente contexto legal y jurisprudencial.\n"
            f"Pregunta: {pregunta}\n"
            f"Contexto legal:\n{contexto}\n"
            f"Respuesta:"
        )
        return llm.invoke(prompt).content
