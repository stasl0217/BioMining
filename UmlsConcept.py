class UmlsConcept:
    """
    one UmlsConcept object can correspond to multiple ids or XML elements in one document.
    """
    def __init__(self, CUI, preferred_text):
        # Concept Unique Identifier in UMLS (consistent across different schemas)
        self.CUI = CUI  # string, like 'C0007226' (7 digits following 'C')
        self.preferred_text=preferred_text  # name
