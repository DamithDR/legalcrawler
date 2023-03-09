import json
import shutil
from os import listdir
from os.path import isfile, join

deduped_set = set()
list_to_keep = []
with open('possible_duplicates.json') as json_file:
    duplicates = dict(json.load(json_file))

    no_duplicates = 0
    unique_cases = []
    for key in duplicates.keys():
        if len(duplicates[key]) == 0:
            no_duplicates += 1
            unique_cases.append(key)
        else:
            dups = list(duplicates[key])
            if key not in deduped_set:
                list_to_keep.append(key)
            deduped_set.update(dups)
            deduped_set.add(key)

    print(f'No of unique cases = {no_duplicates}')
    print(f'list to keep {len(list_to_keep)}')

dataset_with_br_path = 'dataset/processed_with_br/filtered'
dataset_without_br_path = 'dataset/processed_without_br/filtered'

copy_path_with_br = 'dataset/processed_with_br/filtered/deduplicated'
copy_path_without_br = 'dataset/processed_without_br/filtered/deduplicated'

keeping_set = set()
keeping_set.update(list_to_keep)
keeping_set.update(unique_cases)

for file in keeping_set:
    print(f'Processing : {file}')
    shutil.copy(dataset_without_br_path + '/' + file, copy_path_without_br + '/' + file)
    shutil.copy(dataset_with_br_path + '/' + file, copy_path_with_br + '/' + file)

print("Done")
