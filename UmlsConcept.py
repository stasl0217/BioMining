class UmlsConcept:
    """
    one UmlsConcept object can correspond to multiple ids or XML elements in one document.
    """
    def __init__(self, CUI, preferred_text):
        self.CUI = CUI  # CUI for UMLS (consistent across different schemas)
        self.preferred_text=preferred_text  # name
