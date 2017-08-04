# coding: utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join
from UmlsConcept import UmlsConcept
from ConceptMention import ConceptMention

xmldir = r'C:\Users\sinte\Desktop\test\output_umls'
files = [join(xmldir, f) for f in listdir(xmldir) if isfile(join(xmldir, f))]

# typeID = index
types = ['org.apache.ctakes.typesystem.type.textsem.MedicationMention',
         'org.apache.ctakes.typesystem.type.textsem.DiseaseDisorderMention',
         'org.apache.ctakes.typesystem.type.textsem.ProcedureMention',
         'org.apache.ctakes.typesystem.type.textsem.SignSymptomMention',
         'org.apache.ctakes.typesystem.type.textsem.AnatomicalSiteMention']
N = len(types)


def scan_FSArrays(root):
    '''
    scan the whole XML element tree for ONCE,
    and save all FSArrays in a dictionary.
    :param root: root of XML element tree
    :return: { FSArray_id: [id1, id2, ...] }
    '''
    FSArrays = {}
    for FSArray in tree.iter(tag='uima.cas.FSArray'):
        FSArray_id = FSArray.attrib['_id']
        ids = []
        for child in FSArray:
            ids.append(child.text)
        FSArrays[FSArray_id] = ids
    print(FSArrays)
    return FSArrays


def scan_UmlsConcepts(root):
    '''
    scan the whole XML element tree for ONCE,
    and save all FSArrays in a dictionary.
    :param root: root of XML element tree
    :return concepts: = { id : CUI }
    '''
    concepts = {}  # all UmlsConcepts listed in the XML document
    for ccpt in tree.iter(tag='org.apache.ctakes.typesystem.type.refsem.UmlsConcept'):
        id = ccpt.attrib['_id']
        concepts[id] = UmlsConcept(ccpt.attrib['cui'], ccpt.attrib['preferredText'])
    print(concepts)
    return concepts


def extract_concept(ccptmention_dict, FSArrays, concepts):
    '''

    :param ccptmention_dict:
    XML attributes stored in a dict.
    This element MUST be an Named Entity mention element whose tag is in @types.
    The original XML element content ( the input is its attributes) can be like:
    <org.apache.ctakes.typesystem.type.textsem.MedicationMention _indexed="1" _id="2608" _ref_sofa="3" begin="337" end="344" id="16" _ref_ontologyConceptArr="2602" typeID="1" segmentID="SIMPLE_SEGMENT" discoveryTechnique="1" confidence="0.22500001" polarity="1" uncertainty="0" conditional="false" generic="false" subject="patient" historyOf="0" _ref_medicationFrequency="3744" _ref_medicationStatusChange="3711" _ref_medicationStrength="3778" _ref_startDate="3827"/>
    :return:
    :raise:
    KeyError, IndexError
    '''
    try:
        mention_id = ccptmention_dict['_id']
        type_id = int(ccptmention_dict['typeID'])
        begin = int(ccptmention_dict['begin'])  # beginning position of the phrase in the original text
        end = int(ccptmention_dict['end'])
        FSArray_id = ccptmention_dict['_ref_ontologyConceptArr']

        # there may be multiple UmlsConcept ids in one FSArray
        # However, in this case, they should all point to ONE entity in UMLS
        # with different code in different schemas but the same CUI
        umls_ids = FSArrays[FSArray_id]  # list
        if len(umls_ids) > 0:
            umls_id = umls_ids[0]
            umls = concepts[umls_id]  # UmlsConcept object
            # last row may raise KeyError (if concepts passed in are not right)
            concept_mention = ConceptMention(mention_id, type_id, begin, end, umls)
            return concept_mention

        else:
            # normally there shouldn't be an empty FSArray
            raise IndexError('empty FSArray:' + str(FSArray_id))

    except KeyError:
        print(ccptmention_dict)
        print('trouble when trying to extract concept from the concept-mentioning element')


f = files[0]  # TODO: use loop

# create an element tree for this XML file
tree = ET.ElementTree(file=f)
root = tree.getroot()  # get the root element as Element object

FSArrays = scan_FSArrays(tree)
# TODO: exception handling
UmlsConcepts = scan_UmlsConcepts(tree)

concept_mentions = []

# extract all Umls Concept from Named Entity (concept) mentions
for child in root:
    tag = child.tag
    for typeID in range(0, N):
        if tag == types[typeID]:
            # found the Named Entity (concept) mention element
            NEmention_element = child.attrib  # XML content (dictionary)
            mention = extract_concept(NEmention_element, FSArrays, UmlsConcepts)  # UmlsConcept (with position info)
            if mention is not None:
                mention.show()
                concept_mentions.append(mention)
