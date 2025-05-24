import streamlit as st
from collections import deque
import pandas as pd
import datetime

# --- Mockups / Simulaciones ---
CORPUS_LEGAL = {
    "¿Qué es una marca?": [
        {"fuente": "Ley 17/2001, de Marcas, Art. 4", "texto": "La marca es todo signo susceptible de representación gráfica que sirva para distinguir en el mercado los productos o servicios de una empresa de los de otras."},
        {"fuente": "Sentencia TJUE C-104/01", "texto": "Requisitos para la protección de la marca."}
    ],
    "¿Cuándo puede una marca ser declarada nula?": [
        {"fuente": "Ley 17/2001, de Marcas, Art. 51", "texto": "Serán nulas las marcas registradas contraviniendo los requisitos del artículo 5 y siguientes."},
        {"fuente": "Manual OEPM", "texto": "Ejemplos prácticos sobre nulidad de marca."}
    ]
}

ONTOLOGIA_PI = {
    "Marca": ["Definición", "Registro", "Nulidad", "Oposición"],
    "Derechos de autor": ["Obra", "Derechos morales", "Derechos patrimoniales", "Duración"],
    "Patente": ["Invención", "Solicitud", "Concesión", "Nulidad"],
}

def pathrag_simulator(pregunta):
    """Mockup de recuperación tipo PathRAG"""
    # Busca por coincidencia sencilla
    for key, docs in CORPUS_LEGAL.items():
        if pregunta.lower() in key.lower():
            return docs
    return [{"fuente": "No encontrada", "texto": "No se han encontrado fuentes directas en el corpus legal. Considere revisar manualmente en el BOE y bases jurídicas."}]

def validador_epistemico(respuesta):
    """Mockup: siempre valida, pero muestra explicación."""
    if respuesta["fuente"] == "No encontrada":
        return False, "No se ha encontrado una fuente legal directa para esta subpregunta."
    return True, f"Respaldada por: {respuesta['fuente']}"

# --- Generador de árbol de razonamiento (Inquiry Engine) ---
def inquiry_tree(pregunta, max_depth=2, max_width=2):
    def expand(nodo, depth):
        if depth >= max_depth:
            return {}
        hijos = {}
        for i in range(1, max_width + 1):
            subq = f"Subpregunta {depth+1}.{i} sobre '{nodo}'"
            hijos[subq] = expand(subq, depth + 1)
        return hijos
    return {pregunta: expand(pregunta, 0)}

# --- Contextual Generator (Simulación) ---
def contextual_generator(pregunta):
    docs = pathrag_simulator(pregunta)
    respuestas = []
    for doc in docs:
        ok, val = validador_epistemico(doc)
        respuestas.append({
            "pregunta": pregunta,
            "respuesta": doc["texto"],
            "fuente": doc["fuente"],
            "validacion": val
        })
    return respuestas

# --- Reasoning Tracker ---
if "reasoning_tracker" not in st.session_state:
    st.session_state.reasoning_tracker = []

def add_to_reasoning_tracker(registro):
    st.session_state.reasoning_tracker.append(registro)

# --- App Frontend ---
st.title("MVP Código Deliberativo: Derecho de Propiedad Intelectual")
st.markdown("""
**¿Qué hace esta aplicación?**  
Descompone tu pregunta jurídica en un árbol de razonamiento, te permite consultar y justificar cada paso, y te da el historial completo (auditable) con referencias legales y doctrinales.

- **Ontología PI:** Mapea conceptos clave y relaciones jurídicas.
- **Corpus legal:** Leyes, sentencias y manuales PI.
- **PathRAG:** Simula cómo se buscan y encadenan fuentes relevantes.
- **Reasoning Tracker:** Registra cada paso, decisión y fuente.
""")

st.sidebar.header("Parámetros del Árbol de Indagación")
pregunta_inicial = st.sidebar.text_input("Pregunta jurídica principal", "¿Qué es una marca?")
max_depth = st.sidebar.slider("Profundidad máxima", 1, 4, 2)
max_width = st.sidebar.slider("Anchura máxima", 1, 4, 2)

tree = inquiry_tree(pregunta_inicial, max_depth, max_width)

# --- Función recursiva para mostrar el árbol y permitir consulta de contexto ---
def mostrar_arbol(nodo, hijos):
    with st.expander(nodo, expanded=True):
        if st.button(f"Generar contexto para: {nodo}", key=f"context_{nodo}"):
            respuestas = contextual_generator(nodo)
            for resp in respuestas:
                st.success(f"**Respuesta:** {resp['respuesta']}\n\n**Fuente:** {resp['fuente']}\n\n**Validación:** {resp['validacion']}")
                # Añadir al Reasoning Tracker
                add_to_reasoning_tracker({
                    "Fecha": datetime.datetime.now().isoformat(),
                    "Pregunta": resp["pregunta"],
                    "Respuesta": resp["respuesta"],
                    "Fuente": resp["fuente"],
                    "Validación": resp["validacion"]
                })
        # Recursividad
        for hijo, subhijos in hijos.items():
            mostrar_arbol(hijo, subhijos)

st.header("Árbol de razonamiento generado")
for raiz, hijos in tree.items():
    mostrar_arbol(raiz, hijos)

st.markdown("---")
st.header("Ontología PI (Demo Visual)")
st.json(ONTOLOGIA_PI)

st.markdown("---")
st.header("Reasoning Tracker (Auditoría del razonamiento)")
if st.session_state.reasoning_tracker:
    df = pd.DataFrame(st.session_state.reasoning_tracker)
    st.dataframe(df)
    st.download_button("Descargar Reasoning Tracker (CSV)", df.to_csv(index=False), file_name="reasoning_tracker.csv")
else:
    st.info("No hay pasos aún en el Reasoning Tracker.")

st.markdown("---")
st.header("Roadmap y justificación del MVP")
st.markdown("""
- **Ya permite descomponer y documentar el razonamiento jurídico paso a paso.**
- **Puedes auditar y exportar el razonamiento y las fuentes.**
- **Simula la integración de corpus legal, ontología PI y PathRAG.**
- **Permite aprendizaje y uso profesional desde el primer día.**
- **Siguiente Sprint:** Integrar corpus legal real, añadir PathRAG avanzado, grafo PI navegable, y validación doctrinal automática.
""")
