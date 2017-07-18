# -*- coding: utf-8 -*-   
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
from os.path import join
import re


def mining_pdf(pdf_dir, txt_dir, filename):
    if filename[-4:] != '.pdf':
        return
    fp = open(join(pdf_dir, filename), 'rb')
    # 来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    txtname = filename[:-4] + '.txt'
                    output_path = join(txt_dir, txtname)
                    with open(output_path, 'a') as f:
                        f.write(x.get_text().encode('utf-8') + '\n')
    fp.close()


def text_rep(in_dir, file, out_dir):
    with open(join(in_dir,file), 'r') as f:
        str = f.read()
        pattern = re.compile(r'([^\n])\n([^\n])')
        result = pattern.sub(r'\1\2', str)  # 剔除换行符
        with open(join(out_dir, file), 'w') as fout:
            fout.write(result)
