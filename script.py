#!/usr/bin/python

import sys
import os
import shutil

if len(sys.argv) < 2:
    exit(1)

os.mkdir("folder")

pdfname = sys.argv[1][:-4]
for i in range(10 * 1000):
    shutil.copyfile(pdfname + ".pdf", "folder/" + pdfname + str(i) + ".pdf")
