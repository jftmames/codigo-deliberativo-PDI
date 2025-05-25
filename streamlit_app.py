import streamlit as st
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import generar_contexto
import pandas as pd

st.set_page_config(page_title="MVP Derecho PI - Código Deliberativo", layout="wide")
st.title("Demo MVP - Derecho de la Propiedad Intelectual")
st.markdown("""
Esta demo simula razonamiento jurídico automatizado, con validación epistémica visible.
""")

# --- Configuración
st.sidebar.header("Configura el árbol")
pregunta = st.sidebar.text_input("Pregunta principal", "¿Quién puede ser autor de una obra?")
max_depth = st.sidebar.slider("Profundidad máxima", 1, 3, 2)
max_width = st.sidebar.slider("Anchura máxima", 1, 4, 2)

# --- Generación de árbol
iq = InquiryEngine(pregunta, max_depth=max_depth, max_width=max_width)
tree = iq.generate()

# --- Estado inicial del tracker
if "tracker" not in st.session_state:
    st.session_state.tracker = []

# --- Funciones visuales UX mejoradas
def badge_validacion(tipo):
    colores = {
        "validada": ("#28a745", "✅ Validada"),
        "parcial": ("#ffc107", "⚠️ Parcial"),
        "no validada": ("#dc3545", "❌ No validada")
    }
    color, texto = colores.get(tipo, ("gray", tipo))
    return f'<span style="color: white; background-color: {color}; padding: 3px 8px; border-radius: 6px;">{texto}</span>'

def esta_respondido(nodo):
    return any(x["Subpregunta"] == nodo for x in st.session_state.tracker)

def simplificar(nodo):
    return nodo.split("sobre")[-1].strip(" '")

# --- Conteo y progreso

def contar_nodos(tree):
    total = 0
    def contar(hijos):
        nonlocal total
        for _, subhijos in hijos.items():
            total += 1
            contar(subhijos)
    for _, hijos in tree.items():
        total += 1
        contar(hijos)
    return total

def contar_respondidos():
    return len(st.session_state.tracker)

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

# --- Visualización del árbol

colors = ["#F0F8FF", "#E6F2FF", "#D1ECF1"]

def mostrar_arbol(nodo, hijos, nivel=0):
    prefix = " " * nivel
    simplificado = simplificar(nodo)
    check = "✅" if esta_respondido(nodo) else ""

    color = colors[nivel % len(colors)]
    with st.container():
        st.markdown(
            f"""
            <div style='background-color:{color}; padding:10px; border-radius:6px;'>
            <b>{prefix}{simplificado}</b> {check}
            </div>
            """,
            unsafe_allow_html=True
        )

        if esta_respondido(nodo):
            data = [x for x in st.session_state.tracker if x["Subpregunta"] == nodo][0]
            st.markdown(badge_validacion(data["Validación"]), unsafe_allow_html=True)

        if st.button(f"Generar contexto: {simplificado}", key=nodo, disabled=esta_respondido(nodo)):
            with st.spinner("Generando contexto..."):
                data = generar_contexto(nodo)
                st.session_state.tracker.append({
                    "Subpregunta": nodo,
                    "Contexto": data["contexto"],
                    "Fuente": data["fuente"],
                    "Validación": data["validacion"]
                })
                st.success("¡Contexto generado!")

        if esta_respondido(nodo):
            st.info(f"**Contexto:** {data['Contexto']}")
            st.markdown(f"**Fuente:** {data['Fuente']}")

    for hijo, subhijos in hijos.items():
        mostrar_arbol(hijo, subhijos, nivel=nivel+1)

# --- BOTÓN GLOBAL
st.button("🧠 Generar TODO el contexto", on_click=lambda: generar_todo(tree), key="generar_todo")

# --- PROGRESO
st.progress(contar_respondidos() / contar_nodos(tree), text=f"Progreso: {contar_respondidos()}/{contar_nodos(tree)} respondidos")

# --- ÁRBOL DE RAZONAMIENTO
st.subheader("🔍 Árbol de razonamiento jurídico")
for raiz, hijos in tree.items():
    mostrar_arbol(raiz, hijos)

# --- TRACKER
st.subheader("🗂️ Reasoning Tracker (historial de pasos)")
if contar_respondidos() > 0:
    df = pd.DataFrame(st.session_state.tracker)
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇️ Descargar CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="reasoning_tracker.csv")
else:
    st.info("No hay pasos registrados todavía. Pulsa en 'Generar contexto' para comenzar.")

# --- EXPLICACIONES
with st.expander("ℹ️ ¿Qué es la validación epistémica?"):
    st.write("""
    - ✅ Validada: Basada en norma legal o sentencia oficial.
    - ⚠️ Parcial: Basada en doctrina o interpretación, no vinculante.
    - ❌ No validada: No hay respaldo legal claro; puede ser una hipótesis.
    """)

with st.expander("📘 ¿Qué simula este MVP?"):
    st.write("""
    - Árbol deliberativo de razonamiento jurídico.
    - Generación automática de contexto.
    - Validación epistémica.
    - Historial descargable de cada paso.
    - Preparado para conectar con corpus legal, grafo PathRAG y LLM reales.
    """)

st.markdown("""
---
**🔧 Roadmap:**
- Conexión con BOE, OEPM y TJUE.
- Grafo legal PathRAG especializado en PI.
- LLM jurídico validado.
- Explicabilidad y trazabilidad completa.
---
""")
