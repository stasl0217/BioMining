class ConceptMention:
    def __init__(self, id, typeID, begin, end, umls):
        """
        :param id: id of the ConceptMention element
        :param typeID: int. as might be used as array index
        :param begin: int. beginning position of this concept in the text
        :param end: int
        :param umls: UmlsConcept object
        """
        self.id = id  # string
        self.typeID = typeID  # int. as might be used as array index
        self.begin = begin  # int
        self.end = end  # int
        self.umls = umls  # Umlsconcept object

    def show(self):
        # TODO
        print('*** CONCEPT MENTION ***')
        print('id: ' + self.id)
        print('UMLS preferred text: ' + self.umls.preferred_text)
        print('typeId: ' + str(self.typeID))
        print('UMLS CUI:' + self.umls.CUI)
        print('begin: ' + str(self.begin))
        print('end: ' + str(self.end))
        print('*** END ***')
        print('')
