import streamlit as st
import pandas as pd
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import generar_contexto

# CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Código Deliberativo – PI", layout="wide")
st.title("📚 MVP – Derecho de la Propiedad Intelectual")
st.markdown("Simulación de razonamiento jurídico con validación epistémica auditada.")

# SIDEBAR – Configuración
st.sidebar.header("⚙️ Configuración")
pregunta = st.sidebar.text_input("Pregunta principal", "¿Quién puede ser autor de una obra?")
max_depth = st.sidebar.slider("Profundidad", 1, 3, 2)
max_width = st.sidebar.slider("Anchura", 1, 4, 2)

ie = InquiryEngine(pregunta, max_depth=max_depth, max_width=max_width)
tree = ie.generate()

# TRACKER DE RAZONAMIENTO
if "tracker" not in st.session_state:
    st.session_state.tracker = []

# FUNCIONES AUXILIARES

def badge_validacion(tipo):
    if tipo == "validada":
        return '<span style="color: white; background-color: #28a745; padding: 3px 8px; border-radius: 6px;">✅ Validada</span>'
    elif tipo == "parcial":
        return '<span style="color: black; background-color: #ffc107; padding: 3px 8px; border-radius: 6px;">⚠️ Parcial</span>'
    else:
        return '<span style="color: white; background-color: #dc3545; padding: 3px 8px; border-radius: 6px;">❌ No validada</span>'

def esta_respondido(nodo):
    return any(x["Subpregunta"] == nodo for x in st.session_state.tracker)

def contar_nodos(tree):
    total = 0
    def contar(hijos):
        nonlocal total
        for nodo, subhijos in hijos.items():
            total += 1
            contar(subhijos)
    for raiz, hijos in tree.items():
        total += 1
        contar(hijos)
    return total

def contar_respondidos():
    return len(st.session_state.tracker)

# GENERAR TODO
def generar_todo(tree):
    def gen(hijos):
        for nodo, subhijos in hijos.items():
            if not esta_respondido(nodo):
                data = generar_contexto(nodo)
                st.session_state.tracker.append({
                    "Subpregunta": nodo,
                    "Contexto": data["contexto"],
                    "Fuente": data["fuente"],
                    "Validación": data["validacion"]
                })
            gen(subhijos)
    for raiz, hijos in tree.items():
        if not esta_respondido(raiz):
            data = generar_contexto(raiz)
            st.session_state.tracker.append({
                "Subpregunta": raiz,
                "Contexto": data["contexto"],
                "Fuente": data["fuente"],
                "Validación": data["validacion"]
            })
        gen(hijos)

# VISUALIZACIÓN DE ÁRBOL
def mostrar_arbol(nodo, hijos, nivel=0):
    margen = "  " * nivel
    data = next((x for x in st.session_state.tracker if x["Subpregunta"] == nodo), None)

    with st.container():
        col1, col2 = st.columns([9, 1])
        with col1:
            st.markdown(f"{margen}🔹 **{nodo}**")
        with col2:
            if data:
                st.markdown(badge_validacion(data["Validación"]), unsafe_allow_html=True)

        if data:
            st.info(f"{margen}📘 *{data['Contexto']}*")
            st.markdown(f"{margen}🔗 **Fuente:** {data['Fuente']}")
        else:
            if st.button(f"🧠 Generar contexto para: {nodo}", key=f"gen_{nodo}"):
                with st.spinner("Generando contexto..."):
                    nuevo = generar_contexto(nodo)
                    st.session_state.tracker.append({
                        "Subpregunta": nodo,
                        "Contexto": nuevo["contexto"],
                        "Fuente": nuevo["fuente"],
                        "Validación": nuevo["validacion"]
                    })
                    st.rerun()

    for hijo, subhijos in hijos.items():
        mostrar_arbol(hijo, subhijos, nivel + 1)

# BOTÓN GLOBAL
st.button("🧠 Generar TODO el contexto", on_click=lambda: generar_todo(tree), type="primary")

# BARRA DE PROGRESO (fix aplicado aquí)
total = contar_nodos(tree)
respondidos = contar_respondidos()
progreso = min(respondidos / total, 1.0) if total else 0
st.progress(progreso, text=f"Progreso: {respondidos}/{total} respondidos")

# ÁRBOL
st.subheader("🔍 Árbol de razonamiento jurídico")
for raiz, hijos in tree.items():
    mostrar_arbol(raiz, hijos)

# TRACKER
st.subheader("🧾 Reasoning Tracker")
if respondidos > 0:
    df = pd.DataFrame(st.session_state.tracker)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar como CSV", data=csv, file_name="reasoning_tracker.csv", mime="text/csv")
else:
    st.info("Aún no hay pasos registrados.")

# EXPLICACIONES
with st.expander("¿Qué es la validación epistémica?"):
    st.markdown("""
    - ✅ **Validada**: Hay respaldo legal o jurisprudencial claro.
    - ⚠️ **Parcial**: Respaldada por doctrina o interpretación indirecta.
    - ❌ **No validada**: Hipótesis no respaldada por fuentes jurídicas.
    """)

with st.expander("¿Qué simula este MVP?"):
    st.markdown("""
    1. Estructura lógica tipo árbol.
    2. Genera contexto para cada nodo (simulado).
    3. Añade fuente y validación epistémica.
    4. Permite exportar el razonamiento.
    5. Prepara la integración futura con LLM, PathRAG, corpus legal.
    """)

with st.expander("¿Qué es el Reasoning Tracker?"):
    st.markdown("""
    - Registra cada paso, fuente y nivel de validación.
    - Permite auditar decisiones jurídicas generadas.
    """)

