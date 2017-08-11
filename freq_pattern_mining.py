"""
This script is to be used for spark.

== Example
MASTER=local[4] [SPARK_HOME]/bin/spark-submit freq_pattern_mining.py
MASTER=SCAI01.CS.UCLA.EDU:7077 [SPARK_HOME]/bin/spark-submit freq_pattern_mining.py
"""

from pyspark import SparkConf, SparkContext
from pyspark.mllib.fpm import FPGrowth
import csv

conf = SparkConf().setAppName("BioFreqPattern")
sc = SparkContext(conf=conf)


def main():
    itemsets_path1 = "./itemsets.csv"
    itemsets = sc.textFile(itemsets_path1).map(lambda line: line.strip().split('\t')).map(
        lambda x: list(set(x)))  # items must be unique
    model = FPGrowth.train(itemsets, minSupport=0.0008)  # freq=50
    result = model.freqItemsets().collect()

    with open('./freq.csv', 'w') as fout:
        with open('./frqitems.csv', 'w') as fout2:
            for freqitemset in result:
                it = freqitemset.items  # list
                freq = freqitemset.freq
                for CUI in it:
                    fout.write(CUI + '\t')
                fout.write("\n")
                fout2.write(str(freq))
                fout2.write('\n')


if __name__ == "__main__":
    main()
