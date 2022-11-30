import os.path

from PyPDF2 import PdfReader

pdf = os.path.join("..", "downloads", "_uk_cases_CAT_2012_19.pdf") #example
reader = PdfReader(pdf)
page = reader.pages[0]
print(page.extract_text())
