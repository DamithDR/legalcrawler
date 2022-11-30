import os
from os import listdir
from os.path import isfile, join

import docx


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


dir_list = ['westlaw/downloads/hk/docs', 'westlaw/downloads/in/docs', 'westlaw/downloads/my/docs',
            'westlaw/downloads/nz/docs']
split_sent_list = ['© 2022 Thomson Reuters', '© 2019 Thomson Reuters South Asia Private Limited',
                   '© 2019 Thomson Reuters Asia Sdn Bhd (Co. Reg No. 1278218-W)', '© 2022 Thomson Reuters']

total_cases = 0
for path, split_text in zip(dir_list, split_sent_list):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    cases_path = path + '/cases'
    if not os.path.isdir(cases_path):
        os.mkdir(cases_path)

    case_number = 1
    for file in files:
        file_path = path + '/' + file
        print(f'processing started file : {file_path}')
        content = getText(file_path)

        split = content.split(split_text)

        for i in range(0, len(split)):
            save_path = cases_path + '/' + str(case_number) + '.txt'
            paragraphs = []
            with open(save_path, 'w') as f:
                case = split[i].strip()
                if len(case) > 0:
                    f.write(case)
                    case_number += 1
                    total_cases += 1
        print(f'processing finished file : {file_path} with total cases {case_number}')

print(f'total cases processed {total_cases}')
