import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import docx


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


dir_list = ['elitigation/downloads/docs']

cases_to_remove = []

total_cases = 0
for path in dir_list:
    files = [f for f in listdir(path) if isfile(join(path, f))]
    cases_path = path + '/cases'
    if not os.path.isdir(cases_path):
        os.mkdir(cases_path)

    case_number = 1
    for file in files:
        file_path = path + '/' + file
        print(f'processing started file : {file_path}')
        content = getText(file_path)
        save_path = cases_path + '/' + str(case_number) + '.txt'
        with open(save_path, 'w') as f:
            case = content.strip()
            if len(case) > 0:
                f.write(case)
                case_number += 1
                total_cases += 1
            else:
                cases_to_remove.append(file_path)

        print(f'processing finished file : {file_path} with total cases {case_number}')
df = pd.DataFrame(cases_to_remove)
df.to_csv('cases_to_remove_elitigation.csv')
print(f'total cases processed {total_cases}')
