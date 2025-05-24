import streamlit as st
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import ContextualGenerator
import pandas as pd

st.set_page_config(page_title="MVP Derecho PI – Código Deliberativo", layout="wide")

# === 1. Título y Explicación Introductoria ===
st.title("💡 MVP Derecho de la Propiedad Intelectual – Código Deliberativo")
st.markdown("""
Este demo simula cómo un despacho de abogados o una empresa puede consultar cuestiones jurídicas complejas de propiedad intelectual, desglosándolas en subpreguntas, generando contexto validado y manteniendo **auditoría completa del razonamiento**.  
**Cada paso queda registrado, incluyendo las fuentes legales y la validación epistémica.**
""")

# === 2. Sidebar: Preguntas de ejemplo ===
st.sidebar.header("Ejemplos de preguntas de PI")
ejemplos = [
    "¿Puede una empresa española registrar como marca comunitaria el nombre de un río famoso?",
    "¿Es posible proteger una idea bajo la Ley de Propiedad Intelectual española?",
    "¿Cuándo se considera agotado el derecho de distribución en la UE?",
    "¿Puede el titular de derechos de autor prohibir la reventa de su obra física en España?",
    "¿Qué límites existen para las obras derivadas de una patente europea?",
    "¿Es legal el uso de una obra huérfana en una plataforma online en España?",
    "¿Cómo se determina el carácter distintivo de una marca tridimensional?",
]
if st.sidebar.button("Cargar pregunta de ejemplo"):
    st.session_state.pregunta = ejemplos[0]

pregunta = st.text_area("Introduce aquí tu consulta jurídica:", value=st.session_state.get("pregunta", ""), key="pregunta_input")

# === 3. Razonamiento y tracker ===
if "tracker" not in st.session_state:
    st.session_state.tracker = []

# === 4. Procesamiento: Árbol de Preguntas ===
if st.button("Analizar Pregunta"):
    if not pregunta.strip():
        st.error("Introduce una pregunta para analizar.")
    else:
        st.session_state.tracker = []  # Reinicia el tracker para nueva pregunta
        st.session_state.inquiry = InquiryEngine(pregunta)
        st.session_state.tree = st.session_state.inquiry.generate()
        st.success("Desglose de la pregunta realizado. Ahora puedes generar contexto para cada subpregunta.")
        st.session_state["pregunta"] = pregunta  # Guarda para futuras recargas

tree = st.session_state.get("tree", [])

# === 5. Visualización del Árbol + Contexto + Tracker ===

def display_tree(tree, nivel=0, path=""):
    """Muestra árbol de subpreguntas y contexto generado, con Reasoning Tracker."""
    for nodo in tree:
        subq = nodo["pregunta"]
        hijos = nodo.get("subpreguntas", [])
        key = f"contexto-{path}-{subq[:15]}-{nivel}"
        st.markdown("  " * nivel + f"**{subq}**")
        
        # Botón para generar contexto para cada subpregunta
        if st.button(f"Generar contexto para: {subq}", key=key):
            gen = ContextualGenerator(subq)
            contexto, fuentes, valido = gen.generate()
            st.session_state.tracker.append({
                "Subpregunta": subq,
                "Contexto": contexto,
                "Fuentes": "; ".join(fuentes),
                "Validez epistémica": "✅" if valido else "❌"
            })
            st.success(f"Contexto generado para: {subq}")
            with st.expander("Ver contexto generado", expanded=True):
                st.markdown(contexto)
                st.markdown(f"**Fuentes legales:** {fuentes}")
                st.markdown(f"**Validez epistémica:** {'Sí' if valido else 'No'}")
        
        # Mostrar hijos (subpreguntas anidadas)
        if hijos:
            display_tree(hijos, nivel=nivel+1, path=f"{path}/{nivel}")

if tree:
    st.header("Árbol de Subpreguntas")
    display_tree(tree)
    st.markdown("---")

# === 6. Reasoning Tracker: Historial y exportación ===

if st.session_state.tracker:
    st.header("🧭 Reasoning Tracker (Auditoría del razonamiento)")
    df = pd.DataFrame(st.session_state.tracker)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        label="Descargar Reasoning Tracker como CSV",
        data=df.to_csv(index=False).encode(),
        file_name="reasoning_tracker.csv",
        mime="text/csv"
    )

# === 7. Explicaciones pedagógicas para ANECA, abogados y docentes ===
with st.expander("¿Cómo funciona este MVP? (Explicación para abogados y docentes)"):
    st.markdown("""
**Visión general:**
- La aplicación permite analizar cualquier consulta de propiedad intelectual y desglosarla en subpreguntas, siguiendo la metodología de 'El Código Deliberativo'.
- El usuario puede generar contexto legal relevante para cada subpregunta de manera independiente, validando la respuesta, sus fuentes y su respaldo epistémico.
- Cada acción se registra automáticamente en el Reasoning Tracker para permitir auditoría y transparencia total (muy útil para ANECA y entornos profesionales).

**¿Qué es cada parte?**
- **Árbol de Subpreguntas:** Estructura jerárquica del problema legal, permitiendo atacar el caso desde todas sus dimensiones.
- **Generador de Contexto:** Extrae doctrina, leyes y jurisprudencia relevantes para cada subpregunta, simulando el razonamiento experto de un abogado.
- **Reasoning Tracker:** Registro auditable y exportable de cada paso, fuentes citadas y validación epistémica. Ideal para justificar la calidad del razonamiento y la trazabilidad.
""")
