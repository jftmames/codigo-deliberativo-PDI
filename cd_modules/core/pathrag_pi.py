# cd_modules/core/pathrag_pi.py

class PathRAGPI:
    """
    Simulador de recuperación PathRAG sobre grafo PI. Devuelve contexto relevante.
    """
    def __init__(self):
        # Simulación de corpus legal y nodos del grafo
        self.corpus = {
            "marca comunitaria": "El Reglamento (UE) 2017/1001 regula la marca de la Unión Europea...",
            "nulidad": "Art. 59 Reglamento (UE) 2017/1001: Será declarada la nulidad cuando la marca carezca de distintividad...",
            "distintividad": "Sentencia TJUE Libertel: La distintividad es un requisito esencial para la validez de la marca...",
        }

    def retrieve(self, pregunta):
        # Simula búsqueda por palabras clave en los nodos
        contexto = []
        path = []
        for k, v in self.corpus.items():
            if k in pregunta.lower():
                contexto.append(v)
                path.append(k)
        # Siempre devuelve los tres para el ejemplo
        return "\n".join(self.corpus.values()), list(self.corpus.keys())
