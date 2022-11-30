import json
from os import listdir
from os.path import isfile, join

import numpy as np
import pandas as pd

raw_dataset_path = 'dataset/filtered'

files = [f for f in listdir(raw_dataset_path) if isfile(join(raw_dataset_path, f))]

word_sets = []
for file in files:
    path = raw_dataset_path + '/' + file

    with open(path, 'r') as f:
        word_set = set(f.read().strip().split(' '))
        word_sets.append(word_set)
possible_duplicates = dict()
max_match_percentage = 0.0
average_match_percentage = []
for traverse_key in range(0, len(word_sets)):
    match_percentage_list = []
    dup_list = []
    for key in range(0, len(word_sets)):
        if key != traverse_key:
            key_set = word_sets[key]
            traverse_key_set = word_sets[traverse_key]
            match_percentage = len(traverse_key_set.intersection(key_set)) / len(traverse_key_set)
            match_percentage_list.append(match_percentage)
            if match_percentage > 0.9:
                dup_list.append(files[key])
            possible_duplicates[files[traverse_key]] = dup_list
    mean_match_percentage = np.mean(match_percentage_list)
    average_match_percentage.append(mean_match_percentage)
    print(f'Mean match percentage : for item {traverse_key} is {mean_match_percentage}')

with open('possible_duplicates.json', 'w') as file:
    json.dump(possible_duplicates, file)
df_match = pd.DataFrame({'match_percentage_mean': average_match_percentage})
df_match.to_csv('match_percentages.csv', index=False)
