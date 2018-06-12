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
from multiprocessing import Pool

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
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=1, caching=True, check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

if not os.path.exists('folder'):
    os.mkdir('target')

def convert(infile):
    outfile = open('target/' + infile[:-4] + '.txt', 'w')
    outfile.write(convert_pdf_to_txt('folder/' + infile))

pool = Pool(10)
pool.map(convert, os.listdir('folder'))
