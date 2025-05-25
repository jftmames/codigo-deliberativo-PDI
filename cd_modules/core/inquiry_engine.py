# cd_modules/core/inquiry_engine.py

import streamlit as st
from .consultor_ontologia import generar_subpreguntas_desde_ontologia, buscar_conceptos_relacionados

class InquiryEngine:
    def __init__(self, pregunta, max_depth=2, max_width=2):
        self.pregunta = pregunta
        self.max_depth = max_depth
        self.max_width = max_width

        # Inicializa el Reasoning Tracker si no existe
        if "tracker" not in st.session_state:
            st.session_state.tracker = []

    def _expand(self, nodo, depth):
        if depth >= self.max_depth:
            return {}

        subpreguntas = generar_subpreguntas_desde_ontologia(nodo)
        hijos = {}

        for i, sub in enumerate(subpreguntas[:self.max_width]):
            ruta_ontologica = buscar_conceptos_relacionados(nodo)

            st.session_state.tracker.append({
                "nodo_padre": nodo,
                "subpregunta": sub,
                "nivel": depth,
                "ruta": ruta_ontologica,
                "validacion": "no validada"  # Se puede actualizar luego con análisis real
            })

            hijos[sub] = self._expand(sub, depth + 1)

        return hijos

    def generate(self):
        return {self.pregunta: self._expand(self.pregunta, 0)}
