import os
import shutil
from os import listdir
from os.path import isfile, join

import pandas as pd

df = pd.read_csv('cases_to_consider.csv')

removing_files = list(df.loc[df['remove'] == 'Y']['case_path'])

raw_dataset_path = 'dataset/raw'
filtered_dataset_path = 'dataset/filtered'

files = [f for f in listdir(raw_dataset_path) if isfile(join(raw_dataset_path, f))]
new_paths = []

num = 0
removed = 0
for file in files:
    old_path = raw_dataset_path + '/' + file
    new_path = filtered_dataset_path + '/' + file
    if old_path not in removing_files:
        new_paths.append(new_path)
        shutil.copy(old_path, new_path)
        num += 1
    else:
        removed += 1

print(f'total removed = {removed}')
print(f'total files copied to filter folder = {num}')

cases_to_consider = []
cases_to_consider_no_of_lines = []

# removing parts
unnecessary_lines = [('Page' + str(n)) for n in range(1, 1000)]
unnecessary_lines.append('Judgment Text')
unnecessary_lines.append(
    'This database contains editorial enhancements that are not a part of the original material. The database may also have mistakes or omissions. Users are requested to verify the contents with the relevant original text(s) such as, the certified copy of the judgment, Government Gazettes, etc. Thomson Reuters bears no liability whatsoever for the adequacy, accuracy, satisfactory quality or suitability of the content.')

processed_with_br_dataset = 'dataset/processed_with_br/filtered'
processed_without_br_dataset = 'dataset/processed_without_br/filtered'
line_seperator = '<line_break>'
space = '\n'
num = 1
for path in new_paths:
    print(f'processing case number {num} : {path}')
    num += 1
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
            if line in unnecessary_lines:
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
df.to_csv('cases_to_consider_filtered.csv', index=False)
