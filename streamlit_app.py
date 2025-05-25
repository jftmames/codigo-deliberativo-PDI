import streamlit as st
import pandas as pd

from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import ContextualGenerator

# ---- Explicación de la Aplicación ----
st.title("MVP LexDomus: Deliberación jurídica en Propiedad Intelectual")

st.markdown("""
Este MVP genera un árbol de razonamiento jurídico a partir de tu pregunta, estructurando subpreguntas y simulando respuestas basadas en contexto jurídico.
- **Ontología PI:** El motor organiza conceptos y relaciones propias del Derecho de la Propiedad Intelectual.
- **Corpus legal:** Las respuestas simulan estar basadas en leyes, sentencias y tratados relevantes (BOE, OEPM, TJUE, OMPI, etc).
- **Reasoning Tracker:** Cada paso del razonamiento queda registrado y puede exportarse.
---
""")

# ---- Parámetros del Árbol ----
with st.sidebar:
    st.header("Opciones de árbol")
    max_depth = st.slider("Profundidad máxima", 1, 4, 2)
    max_width = st.slider("Anchura máxima", 1, 4, 2)
    st.info("La profundidad controla cuántos niveles de subpreguntas se generan. La anchura, cuántas subpreguntas por nodo.")

# ---- Pregunta Principal ----
pregunta = st.text_input("Introduce tu pregunta jurídica de PI:", value="¿Puede una marca sonora ser registrada en la Unión Europea?")

if "reasoning_tracker" not in st.session_state:
    st.session_state.reasoning_tracker = []

if st.button("Generar árbol de razonamiento"):
    ie = InquiryEngine(pregunta, max_depth=max_depth, max_width=max_width)
    tree = ie.generate()
    st.session_state.tree = tree
    st.session_state.reasoning_tracker = []  # Reset tracker

if "tree" in st.session_state:
    tree = st.session_state.tree

    # --- Funciones de despliegue de árbol (sin expanders anidados) ---
    def mostrar_arbol_planar(arbol, nivel=0):
        for nodo, hijos in arbol.items():
            st.markdown("&nbsp;"*4*nivel + f"- **{nodo}**", unsafe_allow_html=True)
            # Botón para generar contexto por subpregunta
            if st.button(f"Generar contexto para: {nodo}", key=f"context-{nodo}-{nivel}"):
                # Simulación de contexto
                cg = ContextualGenerator(nodo)
                contexto = cg.get_context()
                st.success(f"**Contexto:** {contexto}")
                # Registrar paso en Reasoning Tracker
                st.session_state.reasoning_tracker.append({
                    "Pregunta/Subpregunta": nodo,
                    "Contexto": contexto,
                    "Nivel": nivel
                })
            if hijos:
                mostrar_arbol_planar(hijos, nivel+1)

    def arbol_a_ascii(arbol, prefijo=""):
        resultado = ""
        nodos = list(arbol.keys())
        for i, nodo in enumerate(nodos):
            ultimo = (i == len(nodos) - 1)
            rama = "└── " if ultimo else "├── "
            resultado += f"{prefijo}{rama}{nodo}\n"
            hijos = arbol[nodo]
            if hijos:
                nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")
                resultado += arbol_a_ascii(hijos, nuevo_prefijo)
        return resultado

    st.subheader("Árbol de razonamiento (visual)")
    mostrar_arbol_planar(tree)

    st.subheader("Árbol de razonamiento (ASCII)")
    st.code(arbol_a_ascii(tree), language="text")

    st.markdown("---")
    st.subheader("Reasoning Tracker (historial de pasos)")
    if st.session_state.reasoning_tracker:
        df = pd.DataFrame(st.session_state.reasoning_tracker)
        st.dataframe(df)
        st.download_button("Descargar Reasoning Tracker como CSV", data=df.to_csv(index=False), file_name="reasoning_tracker.csv", mime="text/csv")
    else:
        st.info("Genera contexto para alguna subpregunta para ver el Reasoning Tracker.")

# ---- Explicación de Ontología PI y Grafo Legal (Mockup visual) ----
with st.expander("¿Qué es la Ontología PI y el Grafo Legal?"):
    st.markdown("""
    - **Ontología PI:** Es un mapa conceptual de los elementos clave de la Propiedad Intelectual (obras, autores, derechos, límites, infracciones, procedimientos).
    - **Grafo Legal:** Representa cómo se conectan conceptos y normas, permitiendo búsquedas de información relevantes para cada consulta.
    - **Ejemplo visual:**  
    """)
    st.image("A_flowchart_visualization_diagram_titled__PI__Ejem.png", caption="Estructura conceptual PI (mockup)")
    st.code("""
    Obra
     ├── Autor
     ├── Derecho moral
     ├── Derecho patrimonial
         └── Licencias
     ├── Infracción
     └── Procedimiento
    """, language="text")

with st.expander("¿Qué fuentes legales consulta el MVP?"):
    st.markdown("""
    - Ley de Marcas, Ley de PI, Directivas y Reglamentos UE
    - BOE, OEPM, ECLI (sentencias), TJUE, OMPI
    - Tratados internacionales (ADPIC, Convenio de París)
    """)

with st.expander("¿Cómo se valida la respuesta?"):
    st.markdown("""
    Cada contexto simulado en el MVP debe estar apoyado en normas, doctrina o jurisprudencia.
    (En el futuro: PathRAG validará automáticamente contra corpus legal + grafo PI.)
    """)

with st.expander("Roadmap de desarrollo (próximos pasos)"):
    st.markdown("""
    1. Conexión real con corpus legal y recuperación automática (PathRAG)
    2. Implementación de validación epistémica estricta
    3. Mejora del Reasoning Tracker y explicación textual automática
    4. Generación automática de informes jurídicos justificando cada paso
    5. Integración de módulos para auditoría y revisión colaborativa
    """)

st.markdown("---")
st.caption("Demo orientada a ANECA, despachos y formación jurídica avanzada. Contacto: [jftamames.gitbook.io/el-codigo-deliberativo](https://jftamames.gitbook.io/el-codigo-deliberativo/)")

