import os.path
import re

from PyPDF2 import PdfReader, PdfFileReader

pdf = os.path.join("..", "downloads", "2002_SGHC_281.pdf")  # example
reader = PdfReader(pdf)

page = reader.pages[0]

# search = re.search('Case Number: 1178/5/7/11',page.extract_text())
# search = re.search('Case Number: [0-9]+/[0-9]+/[0-9]+/[0-9]+', page.extract_text())
text = page.extract_text()
search = re.match('[a-zA-Z]', text)

print(search)

# print(page.extract_text())
