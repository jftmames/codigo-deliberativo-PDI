import streamlit as st

from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.epistemic_navigator import EpistemicNavigator
from cd_modules.core.contextual_generator import ContextualGenerator

st.set_page_config(page_title="Código Deliberativo – MVP", layout="wide")

st.title("Código Deliberativo – MVP")
st.caption("Demo académico: Generación deliberativa, recuperación y contexto jurídico.")

# ───────────── Sidebar para parámetros ─────────────
st.sidebar.header("⚙️ Configuración")
domain = st.sidebar.selectbox("Dominio jurídico", ["Propiedad Intelectual"])
depth = st.sidebar.slider("Profundidad de árbol", 1, 4, 2)
width = st.sidebar.slider("Anchura (sub-preguntas por nivel)", 1, 5, 3)

# ───────────── Entrada de pregunta ─────────────
question = st.text_input("Introduce tu pregunta jurídica:")

if st.button("Generar árbol de deliberación"):
    if not question.strip():
        st.warning("Por favor, introduce una pregunta antes de continuar.")
        st.stop()

    # ───────────── Generar la jerarquía de preguntas ─────────────
    ie = InquiryEngine(question, depth=depth, width=width)
    tree = ie.generate()

    st.subheader("Jerarquía de preguntas generada")
    for nivel, capa in enumerate(tree, start=1):
        padre, hijos = next(iter(capa.items()))
        st.markdown(f"**Nivel {nivel}:** {padre}")
        if hijos:
            for hijo in hijos:
                st.markdown(f"- {hijo}")
        else:
            st.markdown("*Sin sub-preguntas*")

    # ───────────── Recuperar fuentes y generar contexto ─────────────
    nav = EpistemicNavigator()
    cgen = ContextualGenerator()

    st.subheader("Fuentes relevantes y contexto profesional")
    for capa in tree:
        padre, _ = next(iter(capa.items()))
        fuentes = [src for src, _ in nav.search(padre, k=3)]
        with st.expander(f"Fuentes y contexto para: {padre}"):
            st.markdown("**Fuentes relevantes:**")
            for src in fuentes:
                st.markdown(f"- {src}")

            if st.button(f"Generar contexto para: {padre}", key=padre):
                contexto = cgen.generate(padre, fuentes)
                st.markdown("**Respuesta profesional generada:**")
                st.success(contexto)

    st.info("Puedes cambiar la profundidad/anchura y volver a generar para explorar otros caminos deliberativos.")

else:
    st.info("Introduce una pregunta y pulsa el botón para empezar.")

