import streamlit as st
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import ContextualGenerator
import pandas as pd

# ------------------------------
# Explicaciones y roadmap
st.title("MVP Legal: Deliberador PI para Propiedad Intelectual")
st.markdown("""
**¿Qué hace la app?**

- Genera un **árbol de razonamiento** sobre una pregunta de Propiedad Intelectual (PI).
- Permite pedir **contexto legal** para cada subpregunta, basado en doctrina y jurisprudencia simulada.
- Registra todo el proceso en un **Reasoning Tracker** (tabla y descarga CSV).
- Justifica cada paso para abogados, docentes y empresas.

---

**Backend simulado**:
- Grafo PI: Estructura jerárquica de conceptos (ver abajo).
- PathRAG: Recuperación de fuentes legales simulada (mockup, para próxima versión).
- Validación epistémica y jurisprudencia: Simulada.
""")

# Mostrar grafo PI (ASCII)
st.subheader("Ontología PI (simulada)")
st.code("""
PI (Propiedad Intelectual)
 ├── Obra
 │     ├── Autor
 │     ├── Derecho Moral
 │     ├── Derecho Patrimonial
 │     └── Licencia / Cesión
 ├── Marca
 │     ├── Marca Sonora
 │     └── Marca Figurativa
 ├── Patente
 │     └── Invención
 ├── Infracción
 └── Jurisprudencia/Procedimiento
""", language="text")

# ------------------------------
# Parámetros de árbol
st.sidebar.header("Configuración del árbol de razonamiento")
pregunta_inicial = st.sidebar.text_input("Pregunta raíz (ejemplo: ¿Qué es una marca comunitaria?)", value="¿Qué es una marca comunitaria?")
max_depth = st.sidebar.slider("Niveles de profundidad", 1, 3, 2)
max_width = st.sidebar.slider("Preguntas por nivel", 1, 4, 2)

# Inicializa motor y Reasoning Tracker
if "tracker" not in st.session_state:
    st.session_state.tracker = []

ie = InquiryEngine(pregunta_inicial, max_depth=max_depth, max_width=max_width)
tree = ie.generate()

st.header("Árbol de razonamiento (simulado)")
st.caption("Haz clic en cada subpregunta para pedir el contexto legal y doctrinal específico.")

def mostrar_arbol(nodo, hijos, nivel=0):
    for subpregunta, subhijos in hijos.items():
        key = f"{subpregunta}-{nivel}"
        with st.container():
            st.markdown(f"{' ' * (nivel*4)}• **{subpregunta}**")
            if st.button("Generar contexto", key=key):
                cg = ContextualGenerator(subpregunta)
                contexto = cg.get_context()
                st.success(contexto)
                # Añadir al Reasoning Tracker
                st.session_state.tracker.append({
                    "Pregunta": subpregunta,
                    "Contexto": contexto
                })
            if subhijos:
                mostrar_arbol(subpregunta, subhijos, nivel+1)

# Mostrar raíz y ramas
for raiz, hijos in tree.items():
    st.markdown(f"### {raiz}")
    mostrar_arbol(raiz, hijos)

# ------------------------------
# Reasoning Tracker visible y descargable
st.header("Reasoning Tracker: seguimiento epistémico")
if st.session_state.tracker:
    df = pd.DataFrame(st.session_state.tracker)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Reasoning Tracker (CSV)", data=csv, file_name="reasoning_tracker.csv", mime="text/csv")
else:
    st.info("Aún no se han generado pasos en el Reasoning Tracker.")

# ------------------------------
# Roadmap visible
st.markdown("""
---
#### Roadmap MVP

- [✔️] Árbol deliberativo PI (mockup, ampliable a corpus/LLM).
- [✔️] Contexto legal y doctrinal simulado (PathRAG futuro).
- [✔️] Reasoning Tracker legal, visible y descargable.
- [🟡] Corpus legal y grafo PI ampliables (BOE, OEPM, TJUE, WIPO).
- [🟡] PathRAG y validación epistémica para la próxima release.
""")
