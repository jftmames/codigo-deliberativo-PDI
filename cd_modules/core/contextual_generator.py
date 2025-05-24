# cd_modules/core/contextual_generator.py

class ContextualGenerator:
    """
    Genera contexto legal simulado para una subpregunta dada, citando fuentes legales.
    Devuelve: contexto (str), lista de fuentes (list), y validez epistémica (bool)
    """
    def __init__(self, subpregunta):
        self.subpregunta = subpregunta

    def generate(self):
        # Demo pedagógico: cambia esta lógica por la real cuando integres PathRAG y grafo PI
        ejemplos = {
            "¿Qué es una marca comunitaria?": (
                "Una marca comunitaria (ahora llamada Marca de la Unión Europea) es un título único que ofrece protección en todos los Estados miembros de la UE. Su base legal principal es el Reglamento (UE) 2017/1001.",
                ["Reglamento (UE) 2017/1001", "BOE-A-2009-18532"],
                True
            ),
            "¿Cuándo se considera agotado el derecho de distribución en la UE?": (
                "El derecho de distribución se agota cuando un producto protegido se comercializa por primera vez en el Espacio Económico Europeo con consentimiento del titular. Ver Artículo 21 TRLPI y jurisprudencia TJUE.",
                ["TRLPI art. 21", "Sentencia TJUE C-173/98"],
                True
            ),
        }
        # Devuelve ejemplo si existe, si no genera respuesta ficticia
        contexto, fuentes, valido = ejemplos.get(
            self.subpregunta,
            (
                f"Contexto simulado: análisis jurídico sobre '{self.subpregunta}'. (Este texto es una muestra; consulte legislación aplicable.)",
                ["BOE", "Jurisprudencia relevante"],
                True
            )
        )
        return contexto, fuentes, valido
