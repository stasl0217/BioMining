import csv
import os
import traceback


os.chdir(r'C:\Users\sinte\LULU\lab\biomining')


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


# frequent itemsets
path_it = './result/frqitems.csv'
itemsets = read_itemsets(path_it)
path_freq = './result/frequences.csv'
freq = read_freq(path_freq)
path_dict = './result/concepts.csv'
concepts = read_concepts(path_dict)  # {CUI : preferred text}

N = len(itemsets)
with open('./result/mining_result.txt', 'w') as fout:
    for i in xrange(N):
        itemset = itemsets[i]

        if len(itemset) > 1:
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
                    fout.write(preferred_text + '; ')
                except KeyError as e:
                    traceback.print_exc()
                    print(repr(e))
            fout.write('\n\n')
