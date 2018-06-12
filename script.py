#!/usr/bin/python3

import sys
import os
import shutil
import math
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

if len(sys.argv) < 2:
    exit(1)

if not os.path.exists('folder'):
    os.mkdir('folder')

pdfname = sys.argv[1][:-4]
N = 10 * 1000
no0 = math.ceil(math.log(N, 10))
src = pdfname + '.pdf'
for i in range(N):
    dst = 'folder/' + pdfname + str(i).zfill(no0) + '.pdf'
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, caching=caching, check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

if not os.path.exists('folder'):
    os.mkdir('target')

for infile in os.listdir('folder'):
    outfile = open('target/' + infile[:-4] + '.txt', 'w')
    outfile.write(convert_pdf_to_txt('folder/' + infile))
