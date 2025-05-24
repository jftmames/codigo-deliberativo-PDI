import streamlit as st

# ───────────────────── Imports de tus módulos ─────────────────────
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.epistemic_navigator import EpistemicNavigator

# (Añadirás ContextualGenerator, AdaptiveDialogue y Tracker más adelante)

# ─────────────────── Configuración de página ──────────────────────
st.set_page_config(page_title="Código Deliberativo – MVP", layout="wide")

st.title("Código Deliberativo – MVP")
st.caption("Interfaz inicial – ahora con generador jerárquico de preguntas.")

# ───────────────────────  Barra lateral  ──────────────────────────
st.sidebar.header("⚙️ Configuración")
domain = st.sidebar.selectbox("Dominio jurídico", ["Propiedad Intelectual"])
depth = st.sidebar.slider("Profundidad", 1, 4, 2)
width = st.sidebar.slider("Anchura", 1, 5, 3)

# ────────────────── Entrada de la pregunta ────────────────────────
question = st.text_input("Escribe tu pregunta jurídica aquí 👇")

# ────────────────── Botón principal ───────────────────────────────
if st.button("Iniciar deliberación"):
    if not question.strip():
        st.warning("Por favor, introduce una pregunta.")
        st.stop()

    # ────────── Generar jerarquía de preguntas ──────────
    inq = InquiryEngine(question, depth=depth, width=width)
    tree = inq.generate()

    st.subheader("Jerarquía de preguntas")
    for nivel, capa in enumerate(tree, start=1):
        padre, hijos = next(iter(capa.items()))
        st.markdown(f"**Nivel {nivel}:** {padre}")
        st.markdown("- " + "\n- ".join(hijos) if hijos else "*Sin sub-preguntas*")

    # ────────── Fuentes de ejemplo con Navigator ─────────
    nav = EpistemicNavigator()

    st.subheader("Fuentes sugeridas")
    for capa in tree:
        padre, _ = next(iter(capa.items()))
        fuentes = nav.search(padre, k=3)
        with st.expander(padre):
            st.write(fuentes)

    st.success("✅ Flujo mínimo completado. ¡Seguiremos ampliando!")
