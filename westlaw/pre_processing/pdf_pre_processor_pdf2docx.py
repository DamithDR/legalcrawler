import os.path
from os import listdir
from os.path import isfile, join

from pdf2docx import parse

dir_list = ['westlaw/downloads/hk', 'westlaw/downloads/in', 'westlaw/downloads/my', 'westlaw/downloads/nz']

for path in dir_list:
    files = [f for f in listdir(path) if isfile(join(path, f))]
    docs_dir = path + '/docs'
    if not os.path.isdir(docs_dir):
        os.mkdir(docs_dir)

    for file in files:
        file_path = path + '/' + file
        doc_path = docs_dir + '/' + file.split('.')[0] + '.docx'
        parse(file_path, doc_path)