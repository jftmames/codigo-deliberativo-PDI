import streamlit as st
import pandas as pd
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.informe_tracker import generar_markdown_reporte


# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Demo PI - Código Deliberativo", layout="wide")
st.title("📚 Demo MVP - Derecho de la Propiedad Intelectual")
st.markdown("Esta demo simula razonamiento jurídico automatizado, con validación epistémica visible.")

# --- SIDEBAR: Parámetros del árbol ---
st.sidebar.header("⚙️ Configuración del árbol")
pregunta = st.sidebar.text_input("Pregunta principal", "¿Quién puede ser autor de una obra?")
max_depth = st.sidebar.slider("Profundidad", 1, 3, 2)
max_width = st.sidebar.slider("Anchura", 1, 4, 2)

# --- Inicialización del Reasoning Tracker ---
if "tracker" not in st.session_state:
    st.session_state.tracker = []

# --- Generación del árbol ---
ie = InquiryEngine(pregunta, max_depth=max_depth, max_width=max_width)
tree = ie.generate()

# --- UX: badge de validación ---
def badge_validacion(tipo):
    if tipo == "validada":
        return '<span style="color: white; background-color: #28a745; padding: 3px 8px; border-radius: 6px;">✅ Validada</span>'
    elif tipo == "parcial":
        return '<span style="color: black; background-color: #ffc107; padding: 3px 8px; border-radius: 6px;">⚠️ Parcial</span>'
    else:
        return '<span style="color: white; background-color: #dc3545; padding: 3px 8px; border-radius: 6px;">❌ No validada</span>'

# --- Visualización del árbol deliberativo ---
def mostrar_arbol(nodo, hijos, nivel=0):
    st.markdown(f"{'— ' * nivel}**{nodo}**")

    data = next((x for x in st.session_state.tracker if x["subpregunta"] == nodo), None)
    if data:
        st.markdown(badge_validacion(data["validacion"]), unsafe_allow_html=True)
        if data.get("ruta"):
            for ruta in data["ruta"]:
                st.markdown(f"{' ' * (nivel * 2)}↳ Ruta ontológica: `{' → '.join(ruta)}`")

    for hijo, subhijos in hijos.items():
        mostrar_arbol(hijo, subhijos, nivel + 1)

# --- Mostrar el árbol generado ---
st.subheader("🌳 Árbol de razonamiento legal")
raiz, hijos = list(tree.items())[0]
mostrar_arbol(raiz, hijos)

# --- Exportación del informe ---
if st.session_state.tracker:
    st.subheader("📄 Informe trazable (Markdown)")
    markdown = generar_markdown_reporte(pregunta, st.session_state.tracker)
    st.code(markdown, language="markdown")

    st.download_button(
        label="⬇️ Descargar informe en .md",
        data=markdown,
        file_name="informe_PI.md",
        mime="text/markdown"
    )
