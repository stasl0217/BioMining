"""
== Notions
1. UMLS: Unified Medical Language System (https://www.nlm.nih.gov/research/umls/)
2. CUI: Concept Unique Identifier in UMLS. 'C' followed by 7 digits.

== Input files
(from result_dir)
1. frqitemsets.csv
    CUI1    CUI2    CUI3
    CUI1    CUI4
    ...
2. frequences.csv
    145
    23
    ...


== Output files


== Author
Shirley Chen (shirleychen@cs.ucla.edu)

== Last updated
Aug 16, 2017

"""

import csv
import os
import traceback
from os.path import join

os.chdir(r'C:\Users\sinte\LULU\lab\biomining')

result_dir = './result_para'


class FreqItemset:
    def __init__(self, itemset, freq):
        self.itemset = itemset
        self.frequence = freq


def read_itemsets(path):
    itemsets = []
    with open(path) as f:
        for line in f:
            items = line.rstrip().split('\t')
            itemsets.append(items)
    return itemsets


def read_freq(path):
    freqs = []
    with open(path) as f:
        for line in f:
            freq = int(line)
            freqs.append(freq)
    return freqs


def read_concepts(path):
    """
    :param path:
    :return: concepts { CUI: preferred_text }
    """
    concepts = {}
    with open(path) as f:
        for line in f:
            concept = line.rstrip().split('\t')
            CUI = concept[0]
            preferred_text = concept[1]
            concepts[CUI] = preferred_text
    return concepts


def read_types(path):
    """
    :return: types {typeID, type_text}
    """
    types = {}
    with open(path) as f:
        for line in f:
            l = line.rstrip().split('\t')
            typeID = l[0]
            type_text = l[1]
            types[typeID] = type_text
    return types


def read_concept_types(path):
    """
    :param path:
    :return: concept_types { CUI: typeID }
    """
    concept_types = {}
    with open(path) as f:
        for line in f:
            l = line.rstrip().split('\t')
            CUI = l[0]
            typeID = l[1]
            concept_types[CUI] = typeID
    return concept_types


def read_same_source_concepts(path):
    """

    :param path:
    :return: { CUI1: set(CUI2, CUI3), CUI2: set(CUI1-may appear or not here, CUI4...) ...}
    """
    # TODO: document
    ssc = {}
    with open(path) as f:
        for line in f:
            CUIs = line.rstrip().split('\t')
            # TODO: exceptions
            c1 = CUIs[0]
            c2 = CUIs[1]
            # either of c1, c2 can be key
            # it doesn't affect the search result later
            if ssc.has_key(c1):
                ssc[c1].add(c2)  # add to set
            else:
                ssc[c1] = set([c2])
    return ssc


def is_valid_itemset(itemset, ssc):
    """
    Condition:
    1. length>1
    2. no concepts from the same source
    :param itemset:
    :param ssc: dict, same source concepts
    :return:
    """
    # if len(itemset) <= 1:
    #     return False
    for i in range(len(itemset)):
        for j in range(i + 1, len(itemset)):
            c1 = itemset[i]
            c2 = itemset[j]
            # ssc = {CUI1: [CUI2, CUI3]}
            # key-value sequence is random, so check both as key
            if ssc.has_key(c1) and c2 in ssc[c1]:
                return False
            if ssc.has_key(c2) and c1 in ssc[c2]:
                return False
    return True


def getCUI(item):
    """

    :param item: (0)CUI, '0' for negated concepts
    :return: CUI, negated=True/False
    """
    negated = False
    if item[0] == '0':  # usually 'C'
        negated = True
        CUI = item[1:]
    else:
        CUI = item
    return CUI, negated


def get_concept_text(CUI, negated):
    if concepts.has_key(CUI):
        text = concepts[CUI]
        if negated:
            text = text + '[negated]'
        return text
    else:
        raise KeyError('this concept not in dict: %s' % CUI)


def save_main(filtered_FreqItemsets):
    with open(join(result_dir, 'mining_result.txt'), 'w') as fout:
        with open(join(result_dir, 'mining_result_single.txt'), 'w') as fsingle:
            for it in filtered_FreqItemsets:
                itemset = it.itemset
                fr = it.frequence
                if len(itemset) > 1:
                    fout.write('[freq = %d]\n' % fr)
                    for item in itemset:
                        # look it up by CUI
                        negated = False
                        if item[0] == '0':  # usually 'C'
                            negated = True
                            CUI = item[1:]
                        else:
                            CUI = item
                        try:
                            preferred_text = concepts[CUI]
                            if negated:
                                preferred_text += '[negated]'
                            fout.write(preferred_text + '; ')
                        except KeyError as e:
                            traceback.print_exc()
                            print(repr(e))
                    fout.write('\n\n')
                else:
                    # single item
                    fsingle.write('[freq = %d]\n' % fr)
                    for item in itemset:
                        # look it up by CUI
                        negated = False
                        if item[0] == '0':  # usually 'C'
                            negated = True
                            CUI = item[1:]
                        else:
                            CUI = item
                        try:
                            preferred_text = concepts[CUI]
                            if negated:
                                preferred_text += '[negated]'
                            fsingle.write(preferred_text + '; ')
                        except KeyError as e:
                            traceback.print_exc()
                            print(repr(e))
                    fsingle.write('\n\n')

    with open(join(result_dir, 'mining_result_morethan3.txt'), 'w') as f3:
        for it in filtered_FreqItemsets:
            itemset = it.itemset
            fr = it.frequence
            if len(itemset) >= 3:
                f3.write('[freq = %d]\n' % fr)
                for item in itemset:
                    # look it up by CUI
                    negated = False
                    if item[0] == '0':  # usually 'C'
                        negated = True
                        CUI = item[1:]
                    else:
                        CUI = item
                    try:
                        preferred_text = concepts[CUI]
                        if negated:
                            preferred_text += '[negated]'
                        f3.write(preferred_text + '; ')
                    except KeyError as e:
                        traceback.print_exc()
                        print(repr(e))
                f3.write('\n\n')


def save_keywords_by_cate():

    # print keywords under this type
    keywords = {}  # {(0)CUI: frequence}
    for it in filtered_FreqItemsets:
        for it in filtered_FreqItemsets:
            itemset = it.itemset
            fr = it.frequence
            if len(itemset) == 1:
                keywords[itemset[0]] = fr

    filename = 'keywords_by_cate.txt'
    with open(join(result_dir,filename), 'w') as fout:
        for key, value in types.items():
            typeID = key
            type_text = value
            fout.write('********** %s **********\n' % type_text)

            for it in filtered_FreqItemsets:
                itemset = it.itemset
                fr = it.frequence
                if len(itemset) == 1:
                    # keyword
                    CUI, negated = getCUI(itemset[0])
                    try:
                        its_type = concept_types[CUI]
                        if its_type == typeID:
                            fout.write('[freq = %d] %s\n' % (fr,get_concept_text(CUI, negated)))
                    except KeyError as ke:
                        print(repr(ke))
                        traceback.print_exc()

            fout.write('********** END OF %s **********\n\n\n' % type_text)



if __name__ == "__main__":
    file_itemsets = 'frqitems.csv'
    file_freq = 'frequences.csv'
    itemsets = read_itemsets(join(result_dir, file_itemsets))
    freq = read_freq(join(result_dir, file_freq))

    file_dict = 'concepts.csv'
    concepts = read_concepts(join(result_dir, file_dict))  # {CUI : preferred text}
    file_samesource = 'equa_concepts.csv'
    same_source_concepts = read_same_source_concepts(join(result_dir, file_samesource))

    # read type information into dict
    types = read_types(join(result_dir, 'types.csv'))  # {typeID: type_txt}
    concept_types = read_concept_types(join(result_dir, 'concept_types.csv'))  # {CUI: typeID}

    N = len(itemsets)

    #TODO: save it into file so we can do more without repeating filtering and sorting
    filtered_FreqItemsets = []  # delete itemsets with same source concepts
    for i in xrange(N):
        itemset = itemsets[i]
        fr = freq[i]
        if is_valid_itemset(itemset, same_source_concepts):
            filtered_FreqItemsets.append(FreqItemset(itemset, fr))
            filtered_FreqItemsets.sort(key=lambda x: x.frequence, reverse=True)

    # save_main(concepts, filtered_FreqItemsets)
    save_keywords_by_cate()
