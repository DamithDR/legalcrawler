import os.path

from PyPDF2 import PdfReader
import pdfplumber

pdf = os.path.join("..", "downloads", "test.pdf")  # example

content = ''
with pdfplumber.open(pdf) as read_pdf:
    reader = PdfReader(pdf)
    no_of_pages = reader.getNumPages()

    # first_page = read_pdf.pages[0]
    # pdf_lines = first_page.lines
    for i in range(0, no_of_pages):

        page = read_pdf.pages[i]
        text = page.extract_text().strip()
        if len(text) > 0:
            content += text
        else:
            print("empty")

split = content.split('©2019ThomsonReutersSouthAsiaPrivateLimitedNationalCompanyLawTribunal')

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
