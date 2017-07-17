import os
from os import listdir
from os.path import isfile, join
import pdf_miner

pdf_dir= r'C:\Users\sinte\LULU\lab\biomining\papers'
files=[f for f in listdir(pdf_dir) if isfile(join(pdf_dir, f))]
txt_dir=r'C:\Users\sinte\LULU\lab\biomining\papers_txt'
for f in files:
    pdf_miner.mining_pdf(pdf_dir,txt_dir,f)