'''Python version requirement: py2.7 (python 3 not supported)'''

import os
from os import listdir
from os.path import isfile, join
from pdf_miner import PDF2text_helper
import time

start=time.clock()

pdf_dir= r'C:\Users\sinte\LULU\lab\biomining\unprocessed\pdf'
temp_dir= r'C:\Users\sinte\LULU\lab\biomining\unprocessed\txttemp'
txt_dir=r'C:\Users\sinte\LULU\lab\biomining\unprocessed\txt'

miner=PDF2text_helper(pdf_dir,temp_dir,txt_dir)

files=[f for f in listdir(pdf_dir) if isfile(join(pdf_dir, f))]

for f in files:
    try:
        miner.mining_pdf(f)  # filename without path
    except Exception as e:
        print(f)
        print(repr(e))


end=time.clock()
print('file number: {0}', str(len(files)))
print('time: {0}', str((end-start)/1000000))




