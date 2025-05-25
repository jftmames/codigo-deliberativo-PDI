# File: cd_modules/core/main_engine.py
"""
MainEngine: Orquesta todo el flujo de procesamiento utilizando las funciones y clases reales de cada módulo.
"""

from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.extractor_conceptual import extraer_conceptos
from cd_modules.core.contextual_generator import generar_contexto
from cd_modules.core.pathrag_pi import recuperar_nodo_relevante
from cd_modules.core.epistemic_navigator import EpistemicNavigator
from cd_modules.core.validador_epistemico import validar_contexto
from cd_modules.core.adaptive_dialogue import AdaptiveDialogue
from cd_modules.core.respuesta_juridica import generar_respuesta
from cd_modules.core.reasoning_tracker import ReasoningTracker
from cd_modules.core.informe_tracker import generar_markdown_reporte
from cd_modules.core.consultor_ontologia import obtener_subgrafo  # función para grafo ontológico

class MainEngine:
    def __init__(self):
        # Inicializar componentes que no dependen de la pregunta
        self.navigator = EpistemicNavigator()
        self.dialogue = AdaptiveDialogue()
        self.tracker = ReasoningTracker()

    def process_question(self, question: str, user_context: dict = None) -> dict:
        """
        Flujo simplificado:
         1) Generar subpreguntas (inquiry)
         2) Extraer conceptos
         3) Generar contexto
         4) Recuperar nodo RAG
         5) Buscar fuentes (navigator)
         6) Validar contexto
         7) Formular respuesta jurídica
         8) Tracking y reporte
         9) Mapeo ontológico (subgrafo)
        """
        # 1) Expandir pregunta mediante InquiryEngine
        inquiry = InquiryEngine(question)
        subqs = inquiry.generate()

        # 2) Extraer conceptos clave
        conceptos = extraer_conceptos(question)

        # 3) Generar contexto para cada concepto
        contextos = []
        for concepto in conceptos:
            try:
                ctx = generar_contexto(concepto)
                contextos.append(ctx)
            except Exception:
                contextos.append({"contexto": "", "fuente": "", "validacion": "no validada"})

        # 4) Recuperar nodo relevante (RAG)
        rag_info = recuperar_nodo_relevante(question)

        # 5) Buscar fuentes relevantes
        sources = self.navigator.search(question)

        # 6) Validar contexto para el nodo recuperado
        validaciones = [validar_contexto(rag_info.get("nodo", ""), c.get("contexto", "")) for c in contextos]

        # 7) Formular respuesta jurídica (tomando el primer subpregunta como ejemplo)
        answer = generar_respuesta(question, rag_info.get("nodo", ""), 0)

        # 8) Registrar en tracker
        self.tracker.add_step(question, sources, answer)

        # Generar informe en Markdown
        report = generar_markdown_reporte(question, self.tracker.get_steps())

        # 9) Mapeo ontológico: grafo en formato Dot para visualización
        try:
            ontology_graph = obtener_subgrafo(conceptos)
        except Exception:
            ontology_graph = None

        return {
            'answer': answer,
            'logs': self.tracker.get_steps(),
            'report': report,
            'concepts': conceptos,
            'ontology_graph': ontology_graph,
            'rag_info': rag_info,
            'validations': validaciones,
            'sources': sources
        }


# File: streamlit_app.py
"""
Refactorización de la UI de Streamlit para delegar en MainEngine e incorporar visualización del mapeo ontológico.
"""
import streamlit as st
import json
from cd_modules.core.main_engine import MainEngine

# Configuración inicial
def main():
    st.set_page_config(page_title="Código Deliberativo PDI", layout="wide")
    st.title("Código Deliberativo PDI")

    # Instanciar MainEngine
    engine = MainEngine()

    # Input de usuario
    question = st.text_area("Escribe tu pregunta:")
    user_ctx_raw = st.text_area("Contexto de usuario (JSON, opcional):", height=100)
    user_context = None
    if user_ctx_raw:
        try:
            user_context = json.loads(user_ctx_raw)
        except json.JSONDecodeError:
            st.error("Contexto no es un JSON válido.")
            return

    if st.button("Procesar pregunta"):
        with st.spinner("Procesando..."):
            result = engine.process_question(question, user_context)

        # Mostrar conceptos identificados
        st.subheader("Conceptos identificados")
        if result.get('concepts'):
            st.write(result['concepts'])
        else:
            st.write("No se identificaron conceptos.")

        # Mostrar mapeo ontológico si está disponible
        ontology_graph = result.get('ontology_graph')
        if ontology_graph:
            st.subheader("Mapa Ontológico")
            st.graphviz_chart(ontology_graph)

        st.subheader("Respuesta Jurídica")
        st.write(result['answer'])

        st.subheader("Logs de Razonamiento")
        st.json(result['logs'])

        st.subheader("Informe de Trazabilidad")
        st.markdown(result['report'])

if __name__ == "__main__":
    main()
