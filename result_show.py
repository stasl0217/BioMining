import csv
import os
import traceback
from os.path import join

os.chdir(r'C:\Users\sinte\LULU\lab\biomining')

result_dir = './result'


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


file_itemsets = 'frqitems.csv'
itemsets = read_itemsets(join(result_dir, file_itemsets))
file_freq = 'frequences.csv'
freq = read_freq(join(result_dir, file_freq))
file_dict = 'concepts.csv'
concepts = read_concepts(join(result_dir, file_dict))  # {CUI : preferred text}
file_samesource = 'equa_concepts.csv'
same_source_concepts = read_same_source_concepts(join(result_dir, file_samesource))

N = len(itemsets)
with open('./result/mining_result_with1.txt', 'w') as fout:
    for i in xrange(N):
        itemset = itemsets[i]

        if is_valid_itemset(itemset,same_source_concepts):
            fr = freq[i]
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
