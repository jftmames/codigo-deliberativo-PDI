# cd_modules/core/contextual_generator.py

class ContextualGenerator:
    """
    Simula la generación de contexto legal/doctrinal para una pregunta o subpregunta jurídica.
    """
    # Simulación de un pequeño corpus legal con fuentes y “jurisprudencia”
    CORPUS_SIMULADO = {
        "¿Qué es una marca?": [
            {"tipo": "ley", "fuente": "Ley 17/2001, de Marcas, Art. 4", "texto": "La marca es todo signo susceptible de representación gráfica..."},
            {"tipo": "jurisprudencia", "fuente": "STS 1234/2018", "texto": "La Sala entiende que la marca sirve para diferenciar productos o servicios en el tráfico económico..."}
        ],
        "¿Puede registrarse como marca un color?": [
            {"tipo": "ley", "fuente": "Ley 17/2001, Art. 4.2", "texto": "También podrán constituir marca los colores per se, siempre que sean susceptibles de representación gráfica."},
            {"tipo": "jurisprudencia", "fuente": "TJUE C-104/01 Libertel", "texto": "El TJUE exige que la representación sea clara, precisa, autosuficiente y objetiva para registrar colores."}
        ]
    }

    @classmethod
    def generar_contexto(cls, pregunta):
        """
        Devuelve una lista de respuestas (leyes, jurisprudencia) relevantes para la pregunta.
        """
        docs = cls.CORPUS_SIMULADO.get(pregunta, [])
        if not docs:
            # Simula búsqueda PathRAG en todo el corpus
            for k, v in cls.CORPUS_SIMULADO.items():
                if pregunta.lower() in k.lower():
                    return v
            return [{
                "tipo": "manual", "fuente": "Manual OEPM 2024",
                "texto": "No se encuentra referencia legal directa, se recomienda consultar el Manual de Examen de la OEPM."
            }]
        return docs
