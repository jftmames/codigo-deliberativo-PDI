import streamlit as st

# ──────────────────────────  imports de tus módulos  ──────────────────────────
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.epistemic_navigator import EpistemicNavigator

# (añadirás ContextualGenerator, AdaptiveDialogue y ReasoningTracker más adelante)

# ──────────────────────────  configuración de la página  ──────────────────────
st.set_page_config(page_title="Código Deliberativo – MVP", layout="wide")

st.title("Código Deliberativo – MVP")
st.caption("Interfaz inicial. Integraremos los módulos en breve.")

# ──────────────────────────  barra lateral de ajustes  ────────────────────────
st.sidebar.header("⚙️ Configuración")
domain = st.sidebar.selectbox("Dominio jurídico", ["Propiedad Intelectual"])

# ──────────────────────────  entrada de la pregunta  ──────────────────────────
question = st.text_input("Escribe tu pregunta jurídica aquí 👇")

# ──────────────────────────  botón de inicio  ────────────────────────────────
if st.button("Iniciar deliberación"):
    if not question.strip():
        st.warning("Por favor, introduce una pregunta.")
        st.stop()

    # ----- Lógica provisional solo con Inquiry Engine y Navigator -----
    inq = InquiryEngine(question)
    tree = inq.generate()

    nav = EpistemicNavigator()

    st.subheader("Jerarquía de preguntas")
    st.json(tree)

    st.subheader("Fuentes sugeridas por sub-pregunta")
    for q in tree:
        sources = nav.search(q)
        with st.expander(q):
            st.write(sources)

    st.success("👍  Flujo mínimo completado. ¡Seguiremos ampliando!")
