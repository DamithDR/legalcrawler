import os.path

from PyPDF2 import PdfReader

pdf = os.path.join("..", "downloads", "test.pdf")  # example
reader = PdfReader(pdf)
no_of_pages = reader.getNumPages()

content = ''
for i in range(1, no_of_pages):
    page = reader.pages[i]
    page_content = page.get_contents()
    text = page.extract_text().strip()
    if len(text) > 0:
        content += text
    else:
        print("empty")

split = content.split('© 2019 Thomson Reuters South Asia Private Limited')

case_number = 1
for i in range(0, len(split)):
    path = os.path.join("..", "downloads", "cases-temp", str(case_number) + '.txt')
    paragraphs = []
    with open(path, 'w') as f:
        case = split[i].strip()
        if len(case) > 0:
            f.write(case)
            case_number += 1

print(len(split))
