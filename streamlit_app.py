import streamlit as st
import pandas as pd
from cd_modules.core.inquiry_engine import InquiryEngine
from cd_modules.core.contextual_generator import ContextualGenerator
from cd_modules.core.epistemic_navigator import EpistemicNavigator
from datetime import datetime
import io

# --------- PANEL INICIAL: SOBRE LA DEMO ---------
with st.expander("ℹ️ Sobre esta demo (leer antes de usar)", expanded=True):
    st.markdown("""
**MVP Deliberativo en Derecho de la Propiedad Intelectual**

- Esta demo muestra el flujo y experiencia del prototipo funcional de asistencia deliberativa para Derecho de PI.
- **Componentes reales:** árbol deliberativo, generación de contexto jurídico, Reasoning Tracker (historial y descarga).
- **Componentes simulados:** corpus legal (BOE, OEPM, sentencias, tratados), grafo PI, motor PathRAG, validador epistémico.
- En la versión final, la app integrará búsqueda en bases reales, grafo PI visual, y validación automática de afirmaciones legales.
- Si tienes dudas sobre el roadmap técnico, consulta la documentación o pregunta al presentador.
""")

st.markdown("---")

# --------- MOCKUP VISUAL DEL GRAFO PI FUTURO ---------
with st.expander("📊 Vista previa: Futuro grafo PI (mockup visual)"):
    st.image("https://raw.githubusercontent.com/jftamames/codigo-deliberativo-PDI/main/assets/grafo_pi_mockup.png",
             caption="Ejemplo ilustrativo de cómo el grafo PI mostraría relaciones entre conceptos, leyes y casos.")
    st.caption("En la versión avanzada, este grafo será interactivo y se generará dinámicamente según la consulta.")

# --------- SUGERENCIA DE PREGUNTA PROBLEMÁTICA ---------
with st.expander("🎓 ¿Ejemplo de pregunta compleja para probar?"):
    st.code("¿Es protegible por derecho de autor una base de datos generada parcialmente por IA?")

st.markdown("---")

# --------- INPUT PRINCIPAL DEL USUARIO ---------
st.header("🧩 Consulta jurídica en Propiedad Intelectual")
pregunta = st.text_area("Introduce tu pregunta jurídica (PI):", 
                        placeholder="Ejemplo: ¿Cuáles son los requisitos para registrar una marca de la UE?")

if pregunta:
    # --------- INQUIRY ENGINE: GENERACIÓN DEL ÁRBOL DELIBERATIVO ---------
    st.subheader("🔹 Árbol deliberativo de subpreguntas")
    st.caption("🧠 Este árbol representa la descomposición conceptual de la pregunta en subtemas PI, equivalente a un grafo legal especializado.")

    ie = InquiryEngine(pregunta, depth=2, width=2)
    tree = ie.generate()

    def display_tree(tree, level=0):
        for nodo, hijos in tree.items():
            st.markdown(" " * level + f"- **{nodo}**")
            if hijos:
                display_tree(hijos, level + 1)
    display_tree(tree)

    st.markdown("---")

    # --------- EPISTEMIC NAVIGATOR: FUENTES SIMULADAS ---------
    st.subheader("🔹 Fuentes relevantes para cada subpregunta")
    st.markdown("🔎 *Fuentes simuladas para demo. En producción, la recuperación será sobre BOE, OEPM, sentencias y tratados oficiales.*")

    nav = EpistemicNavigator()
    fuentes_dict = {}
    for padre in tree:
        fuentes = [src for src, _ in nav.search(padre, k=3)]
        fuentes_dict[padre] = fuentes
        st.markdown(f"**{padre}**")
        for fuente in fuentes:
            st.markdown(f"- {fuente}")

    st.markdown("---")

    # --------- CONTEXTUAL GENERATOR: RESPUESTA A SUBPREGUNTAS ---------
    st.subheader("🔹 Generación de contexto jurídico (simulada)")
    st.caption("📑 Contexto generado con IA adaptada a PI. En el futuro, cada respuesta será validada automáticamente por el corpus legal.")

    cg = ContextualGenerator()
    respuestas = {}
    for padre in tree:
        if st.button(f"Generar contexto para: {padre}"):
            contexto = cg.generate(padre, fuentes_dict[padre])
            respuestas[padre] = contexto
            st.markdown(f"**Respuesta generada:** {contexto}")

    st.markdown("---")

    # --------- REASONING TRACKER Y EXPORTACIÓN ---------
    st.subheader("🔹 Reasoning Tracker: Historial y descarga")
    st.markdown("📝 Puedes descargar todo tu razonamiento y fuentes como CSV. Este registro es clave para auditoría, docencia y compliance.")

    tracker_data = []
    for padre in tree:
        tracker_data.append({
            "subpregunta": padre,
            "fuentes": "; ".join(fuentes_dict[padre]),
            "respuesta": respuestas.get(padre, "")
        })
    df_tracker = pd.DataFrame(tracker_data)

    csv_buffer = io.StringIO()
    df_tracker.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Descargar Reasoning Tracker (CSV)",
        data=csv_buffer.getvalue(),
        file_name=f"reasoning_tracker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv'
    )

st.info("""
🔒 **Demo:** Algunas funcionalidades avanzadas (grafo PI real, PathRAG, validación epistémica automática) están en fase de desarrollo.  
Consulta la documentación del proyecto para más información.
""")
