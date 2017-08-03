# coding: utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

xmldir = r'C:\Users\sinte\Desktop\test\output_umls'
files = [join(xmldir, f) for f in listdir(xmldir) if isfile(join(xmldir, f))]

# typeID = index
types = ['org.apache.ctakes.typesystem.type.textsem.MedicationMention',
              'org.apache.ctakes.typesystem.type.textsem.DiseaseDisorderMention',
              'org.apache.ctakes.typesystem.type.textsem.ProcedureMention',
              'org.apache.ctakes.typesystem.type.textsem.SignSymptomMention',
              'org.apache.ctakes.typesystem.type.textsem.AnatomicalSiteMention']
N = len(types)


def get_FSArray_for_cate(root):
    # TODO: change FSArray_Ids to dictionary {id:cate}
    # scan for elements of each category
    FSArray_Ids = [[] for i in range(N)]  # FSArray id from each category's '_ref_ontologyConceptArr'

    for child in root.iter():
        tag = child.tag
        # save the ontologyConceptArr(id) to FSArray_Ids
        for i in range(0, N):
            if tag == types[i]:
                cate_element = child.attrib  # dictionary
                try:
                    id = cate_element['_ref_ontologyConceptArr']
                    print(id)
                    FSArray_Ids[i].append(id)
                except KeyError:
                    print('cate: ' + types[i])
                    print('ERROR when trying to find the "_ref_ontologyConceptArr"')

    return FSArray_Ids


# create element tree
f = files[0]  # TODO: use for loop

tree = ET.ElementTree(file=f)
root = tree.getroot()  # get the root element as Element object

FSArray_Ids = get_FSArray_for_cate(root)

# find according FSArray and save elements
concept_ids = [[] for i in range(N)]  # a list for each category

for FSArray in root.iter(tag='uima.cas.FSArray'):
    for i in range(N):  # category i
        if FSArray.attrib['_id'] == FSArray_Ids[i]:
            print(FSArray.attrib['_id'])
            for child in FSArray:
                print(child.text)
                concept_ids[i].append(child.text)
