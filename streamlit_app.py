def mostrar_arbol(nodo, hijos, nivel=0):
    margen = "  " * nivel
    data = next((x for x in st.session_state.tracker if x["Subpregunta"] == nodo), None)

    # Separar etiqueta y base para mejor visualización
    if " relacionada con: " in nodo:
        titulo, base = nodo.split(" relacionada con: ", 1)
        display_text = f"{titulo} (sobre: {base})"
    else:
        display_text = nodo

    with st.container():
        col1, col2 = st.columns([9, 1])
        with col1:
            st.markdown(f"{margen}🔹 **{display_text}**")
        with col2:
            if data:
                st.markdown(badge_validacion(data["Validación"]), unsafe_allow_html=True)

        if data:
            st.info(f"{margen}📘 *{data['Contexto']}*")
            st.markdown(f"{margen}🔗 **Fuente:** {data['Fuente']}")
        else:
            if st.button(f"🧠 Generar contexto para: {display_text}", key=f"gen_{nodo}"):
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
