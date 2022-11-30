import os.path
from io import StringIO

from PyPDF2 import PdfReader
# import pdfplumber
from pdfminer.high_level import extract_text, extract_text_to_fp
from pdfminer.layout import LAParams

pdf = os.path.join("..", "downloads", "test-changed.pdf")  # example

# content = ''

# no_of_pages = reader.getNumPages()

output_string = StringIO()
with open(pdf, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

# content = extract_text(pdf)
content = output_string.getvalue().strip()
print(content)
# first_page = read_pdf.pages[0]
# pdf_lines = first_page.lines
# for i in range(0, no_of_pages):
#
#     page = read_pdf.pages[i]
#     text = page.extract_text().strip()
#     if len(text) > 0:
#         content += text
#     else:
#         print("empty")

split = content.split('© 2019 Thomson Reuters South Asia Private Limited')

case_number = 1
for i in range(0, len(split)):
    path = os.path.join("..", "downloads", "cases-temp-new", str(case_number) + '.txt')
    paragraphs = []
    with open(path, 'w') as f:
        case = split[i].strip()
        if len(case) > 0:
            f.write(case)
            case_number += 1

print(len(split))
