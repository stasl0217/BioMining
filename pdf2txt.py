'''Python version requirement: py2.7 (python 3 not supported)'''

import os
from os import listdir
from os.path import isfile, join
import pdf_miner

pdf_dir= r'C:\Users\sinte\LULU\lab\biomining\papers'
files=[f for f in listdir(pdf_dir) if isfile(join(pdf_dir, f))]
txt_dir1=r'C:\Users\sinte\LULU\lab\biomining\txt_temp'
for f in files:
    pdf_miner.mining_pdf(pdf_dir,txt_dir1,f)

txt_files=[f for f in listdir(txt_dir1) if isfile(join(txt_dir1, f))]
txt_dir2=r'C:\Users\sinte\LULU\lab\biomining\txt'
for f in txt_files:
    pdf_miner.text_rep(txt_dir1,f,txt_dir2)

