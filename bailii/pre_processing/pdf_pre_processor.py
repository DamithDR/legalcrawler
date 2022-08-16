import os.path
import re

from PyPDF2 import PdfReader, PdfFileReader

pdf = os.path.join("..", "downloads", "_uk_cases_CAT_2012_19.pdf") #example
reader = PdfFileReader(pdf)
info = reader.getDocumentInfo()

print(info.author)
print(info.title)
# print(info.items())
page = reader.getPage(0)

# search = re.search('Case Number: 1178/5/7/11',page.extract_text())
search = re.search('Case Number: [0-9]+/[0-9]+/[0-9]+/[0-9]+',page.extract_text())

print(search)


# print(page.extract_text())
