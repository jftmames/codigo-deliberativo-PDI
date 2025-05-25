import streamlit as st
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import ContextualGenerator
from cd_modules.core.pathrag_pi import PathRAGPI
from cd_modules.core.validador_epistemico import validador_epistemico
import pandas as pd

st.set_page_config(page_title="MVP PI - Código Deliberativo", layout="wide")

st.title("MVP Propiedad Intelectual – Código Deliberativo")

st.markdown("""
**Demo: Resolución jurídica guiada y auditada con IA**
- Grafo PI + PathRAG + Corpus legal + LLM + Validador epistémico + Reasoning Tracker
""")

# --- Parámetros ---
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("OpenAI API Key", type="password")
pregunta = st.text_input("Pregunta jurídica sobre PI", "¿Puede declararse nula una marca comunitaria por falta de distintividad?")

max_depth = st.slider("Profundidad del árbol", 1, 3, 2)
max_width = st.slider("Anchura por nivel", 1, 3, 2)

if not openai_api_key:
    st.warning("Introduce tu clave de OpenAI para probar la integración real.")
    st.stop()

# --- MVP Backend ---
ie = InquiryEngine(pregunta, max_depth=max_depth, max_width=max_width)
tree = ie.generate()

pathrag = PathRAGPI()
contextual_gen = ContextualGenerator(api_key=openai_api_key)
reasoning_tracker = []

# --- Función recursiva para visualización y demo paso a paso ---
def mostrar_arbol(nodo, hijos, nivel=0):
    st.write("**" + "⮞ " * nivel + nodo + "**")
    if st.button(f"Generar contexto para: {nodo}", key=f"{nodo}_{nivel}"):
        contexto, path = pathrag.retrieve(nodo)
        respuesta = contextual_gen.generar_contexto(nodo, contexto)
        validaciones = validador_epistemico(respuesta, contexto)
        st.success("**Respuesta fundamentada:**\n\n" + respuesta)
        st.info(f"**Camino PathRAG:** {' → '.join(path)}")
        st.info(f"**Validación epistémica:** {'; '.join([f'{k}: ✅' if v else f'{k}: ❌' for k, v in validaciones.items()])}")
        # Añadir al reasoning tracker
        reasoning_tracker.append({
            "pregunta": nodo, "respuesta": respuesta, "contexto": contexto,
            "path": " → ".join(path), "validación": validaciones
        })
    for subnodo, subhijos in hijos.items():
        mostrar_arbol(subnodo, subhijos, nivel + 1)

# --- Mostrar árbol ---
st.header("Árbol de razonamiento jurídico (Inquiry Tree)")
raiz, hijos = list(tree.items())[0]
mostrar_arbol(raiz, hijos)

# --- Reasoning Tracker ---
st.header("Reasoning Tracker (Trazabilidad completa)")
if reasoning_tracker:
    df = pd.DataFrame(reasoning_tracker)
    st.dataframe(df)
    st.download_button("Descargar Reasoning Tracker como CSV", df.to_csv(index=False), "reasoning_tracker.csv")

# --- Ayudas y roadmap ---
with st.expander("¿Cómo funciona este MVP?"):
    st.markdown("""
- **Ontología PI:** El grafo simula relaciones conceptuales clave en Derecho de Marcas.
- **PathRAG:** Recupera solo los conceptos relevantes para cada pregunta.
- **Corpus legal:** Ejemplo con artículos reales del Reglamento (UE) y sentencias.
- **LLM:** OpenAI responde solo con ese contexto legal/jurisprudencial.
- **Validador epistémico:** Marca si la respuesta está bien fundamentada.
- **Reasoning Tracker:** Toda la consulta y sus pasos son trazables y exportables.

**Roadmap:**  
En producción, ampliamos el grafo PI y el corpus legal, y sustituimos la simulación por integración real con bases BOE, OEPM, TJUE, LlamaIndex, etc. El diseño es extensible.
    """)

#with st.expander("Demo visual: Grafo PI y PathRAG (mockup)"):
    #st.image("grafo_pi_pathrag.png", caption="Grafo PI + PathRAG – Relaciones y caminos entre conceptos jurídicos.")

st.info("MVP listo para ANECA y demo profesional. Arquitectura modular, exportable y 100% trazable.")

