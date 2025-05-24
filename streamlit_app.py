import streamlit as st

from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.epistemic_navigator import EpistemicNavigator
from cd_modules.core.contextual_generator import ContextualGenerator

st.set_page_config(page_title="Código Deliberativo – MVP", layout="wide")

st.title("Código Deliberativo – MVP")
st.caption("Demo académico: Generación deliberativa, recuperación y contexto jurídico.")

# --- Sidebar para parámetros ---
st.sidebar.header("⚙️ Configuración")
domain = st.sidebar.selectbox("Dominio jurídico", ["Propiedad Intelectual"])
depth = st.sidebar.slider("Profundidad de árbol", 1, 4, 2)
width = st.sidebar.slider("Anchura (sub-preguntas por nivel)", 1, 5, 3)

# --- Inicializa session_state ---
if "contextos" not in st.session_state:
    st.session_state["contextos"] = {}
if "tracker" not in st.session_state:
    st.session_state["tracker"] = []

# --- Entrada de pregunta ---
question = st.text_input("Introduce tu pregunta jurídica:")

if st.button("Generar árbol de deliberación"):
    if not question.strip():
        st.warning("Por favor, introduce una pregunta antes de continuar.")
        st.stop()

    # Limpia contextos y tracker para nuevo árbol
    st.session_state["contextos"] = {}
    st.session_state["tracker"] = []

    # --- Genera la jerarquía de preguntas ---
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

    # Guarda el árbol en sesión para que persista entre pulsaciones
    st.session_state["tree"] = tree

else:
    tree = st.session_state.get("tree")
    if tree:
        st.subheader("Jerarquía de preguntas generada previamente")
        for nivel, capa in enumerate(tree, start=1):
            padre, hijos = next(iter(capa.items()))
            st.markdown(f"**Nivel {nivel}:** {padre}")
            if hijos:
                for hijo in hijos:
                    st.markdown(f"- {hijo}")
            else:
                st.markdown("*Sin sub-preguntas*")

# --- Recupera fuentes y genera contexto para cada pregunta ---
if tree:
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

            # Botón y lógica con session_state
            if st.button(f"Generar contexto para: {padre}", key=padre):
                contexto = cgen.generate(padre, fuentes)
                st.session_state["contextos"][padre] = contexto
                st.session_state["tracker"].append({
                    "question": padre,
                    "sources": fuentes,
                    "generated_answer": contexto
                })

            # Mostrar SIEMPRE el contexto si ya se ha generado
            if padre in st.session_state["contextos"]:
                st.markdown("**Respuesta profesional generada:**")
                st.success(st.session_state["contextos"][padre])

    # --- Visualizar Reasoning Tracker y métrica EEE ---
    if st.session_state["tracker"]:
        st.subheader("📊 Rastreo y métrica EEE")
        for idx, step in enumerate(st.session_state["tracker"], 1):
            st.markdown(f"**{idx}. Pregunta:** {step['question']}")
            st.markdown(f"**Fuentes:**")
            for src in step['sources']:
                st.markdown(f"- {src}")
            st.markdown(f"**Respuesta generada:** {step['generated_answer']}")
            st.markdown("---")
        total = len(st.session_state["tracker"])
        con_fuentes = sum(1 for step in st.session_state["tracker"] if step['sources'])
        eee = round(100.0 * con_fuentes / total, 2) if total > 0 else 0.0
        st.info(f"EEE: {eee}% de pasos con fuentes asociadas.")

    st.info("Puedes cambiar la profundidad/anchura y volver a generar para explorar otros caminos deliberativos.")

else:
    st.info("Introduce una pregunta y pulsa el botón para empezar.")

