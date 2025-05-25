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

        return {
            'answer': answer,
            'logs': self.tracker.get_steps(),
            'report': report
        }