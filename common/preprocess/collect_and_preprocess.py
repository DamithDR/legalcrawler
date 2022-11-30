import argparse
import os
from os import listdir
from os.path import isfile, join
import shutil

import pandas as pd

parser = argparse.ArgumentParser(
    description='''enable formatting ''')
parser.add_argument('--formatting', required=False, help='enable formatting', default=True)

arguments = parser.parse_args()

cases_paths = ['bailii/downloads/docs/cases', 'elitigation/downloads/docs/cases',
               'search2fedcourt/downloads/docs/cases',
               'westlaw/downloads/hk/docs/cases', 'westlaw/downloads/in/docs/cases', 'westlaw/downloads/my/docs/cases',
               'westlaw/downloads/nz/docs/cases']
prefixs = ['bl', 'el', 'sf', 'wl-hk', 'wl-in', 'wl-my', 'wl-nz']

raw_dataset_path = 'dataset/raw'
processed_with_br_dataset = 'dataset/processed_with_br'
processed_without_br_dataset = 'dataset/processed_without_br'

new_paths = []

for path, prefix in zip(cases_paths, prefixs):
    number = 1
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        old_path = path + '/' + file
        new_path = raw_dataset_path + '/' + prefix + "-" + str(number) + ".txt"
        new_paths.append(new_path)
        shutil.copy(old_path, new_path)
        number += 1

print(f'Total No of Files : {len(new_paths)}')

line_seperator = '<line_break>'
space = '\n'

if arguments.formatting:
    cases_to_consider = []
    cases_to_consider_no_of_lines = []

    # removing parts
    page_numbers = [('Page' + str(n)) for n in range(1, 1000)]

    total_cases = 0
    for path in new_paths:

        if not os.path.isdir(processed_with_br_dataset):
            os.mkdir(processed_with_br_dataset)
        if not os.path.isdir(processed_without_br_dataset):
            os.mkdir(processed_without_br_dataset)

        previous_line = 'start'
        with open(path, 'r') as case:

            case_lines = case.readlines()

            # processing the case
            if len(case_lines) < 15:
                cases_to_consider.append(path)
                cases_to_consider_no_of_lines.append(len(case_lines))

            filtered_lines_with_br = []
            i = 0
            while i < len(case_lines):
                line = case_lines[i].strip().replace('\n', ' ')
                if line.__eq__('Westlaw Asia Delivery Summary'):
                    i += 12  # skip 12 lines
                    previous_line = line
                    continue
                if line in page_numbers:
                    previous_line = line
                    i += 1
                    continue
                if len(line) < 3:
                    previous_line = line
                    i += 1
                    continue
                if len(previous_line) == 0 and len(line) != 0:
                    filtered_lines_with_br.append(line_seperator + space)
                elif len(line) == 0:
                    previous_line = line
                    i += 1
                    continue
                filtered_lines_with_br.append(line + space)
                previous_line = line
                i += 1

            file_name = processed_with_br_dataset + '/' + path.split('/')[len(path.split('/')) - 1]
            with open(file_name, 'w') as nf:
                nf.writelines(filtered_lines_with_br)

            filtered_lines_without_br = list(filter((line_seperator + space).__ne__, filtered_lines_with_br))
            file_name_without_br = processed_without_br_dataset + '/' + path.split('/')[len(path.split('/')) - 1]
            with open(file_name_without_br, 'w') as nf:
                nf.writelines(filtered_lines_without_br)
    df = pd.DataFrame({'case_path': cases_to_consider, 'no_of_lines': cases_to_consider_no_of_lines})
    df.to_csv('cases_to_consider.csv', index=False)
