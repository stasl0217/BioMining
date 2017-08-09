class ConceptMention:
    def __init__(self, id, typeID, begin, end, umls, sentence_list,negation=False):
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
        self.sentence = self.locate_sentence(sentence_list)
        self.negation=negation

    def locate_sentence(self, sentences):
        """
        :param sentences: [ Sentence objects] (ordered by id)
        :return: sentence id
        """
        # binary search
        low = 0
        high = len(sentences) - 1
        while low <= high:
            mid = low + (high - low) / 2  # avoid overflow
            if self.begin < sentences[mid].begin:
                high = mid-1
            elif self.begin > sentences[mid].begin:
                if self.begin <= sentences[mid].end:
                    return sentences[mid].id
                else:
                    low = mid+1
            else:  # self.begin==sentences[mid].begin
                return sentences[mid].id

        return 1

    def show(self):
        print('*** CONCEPT MENTION ***')
        print('id: ' + self.id)
        print('UMLS preferred text: ' + self.umls.preferred_text)
        print('sentence NO.:' + str(self.sentence))
        print('Negated: ' + str(self.negation))
        print('typeId: ' + str(self.typeID))
        print('UMLS CUI:' + self.umls.CUI)
        print('begin: ' + str(self.begin))
        print('end: ' + str(self.end))
        print('*** END ***')
        print('')

    def text(self):
        return '{0} {1}'.format(self.umls.preferred_text, '[negated]' if self.negation else '')