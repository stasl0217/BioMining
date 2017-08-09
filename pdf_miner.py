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
import sys


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
    with open(join(in_dir, file), 'r') as f:
        str = f.read()

        # get rid of the exceptional \n
        pattern = re.compile(r'([^\n])\n([^\n])')
        result = pattern.sub(r'\1\2', str)  # 剔除换行符

        # get rid of invalid XML characters

        with open(join(out_dir, file), 'w') as fout:
            fout.write(result)



def invalid_xml_remove(c):
    """
    Source: https://gist.github.com/lawlesst/4110923
    """
    # http://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
    illegal_unichrs = [(0x00, 0x08), (0x0B, 0x1F), (0x7F, 0x84), (0x86, 0x9F),
                       (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF),
                       (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF),
                       (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                       (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF),
                       (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                       (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF),
                       (0x10FFFE, 0x10FFFF)]

    illegal_ranges = ["%s-%s" % (unichr(low), unichr(high))
                      for (low, high) in illegal_unichrs
                      if low < sys.maxunicode]

    illegal_xml_re = re.compile(u'[%s]' % u''.join(illegal_ranges))
    if illegal_xml_re.search(c) is not None:
        # Replace with space
        return ' '
    else:
        return c


def clean_char(char):
    """
    Source: https://gist.github.com/lawlesst/4110923
    """
    """
    Function for remove invalid XML characters from
    incoming data.
    """
    # Get rid of the ctrl characters first.
    # http://stackoverflow.com/questions/1833873/python-regex-escape-characters
    char = re.sub('\x1b[^m]*m', '', char)
    # Clean up invalid xml
    char = invalid_xml_remove(char)
    replacements = [
        (u'\u201c', '\"'),
        (u'\u201d', '\"'),
        (u"\u001B", ' '),  # http://www.fileformat.info/info/unicode/char/1b/index.htm
        (u"\u0019", ' '),  # http://www.fileformat.info/info/unicode/char/19/index.htm
        (u"\u0016", ' '),  # http://www.fileformat.info/info/unicode/char/16/index.htm
        (u"\u001C", ' '),  # http://www.fileformat.info/info/unicode/char/1c/index.htm
        (u"\u0003", ' '),  # http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=0x
        (u"\u000C", ' ')
    ]
    for rep, new_char in replacements:
        if char == rep:
            # print ord(char), char.encode('ascii', 'ignore')
            return new_char
    return char
