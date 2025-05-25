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
