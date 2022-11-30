import json
import shutil
from os import listdir
from os.path import isfile, join

deduped_set = set()
list_to_keep = []
with open('possible_duplicates.json') as json_file:
    duplicates = dict(json.load(json_file))

    no_duplicates = 0
    for key in duplicates.keys():
        if len(duplicates[key]) == 0:
            no_duplicates += 1
        else:
            dups = list(duplicates[key])
            if key not in deduped_set:
                list_to_keep.append(key)
            deduped_set.update(dups)
            deduped_set.add(key)

    print(f'No of unique cases = {no_duplicates}')
    print(f'list to keep {len(list_to_keep)}')
    print(list_to_keep)

# raw_dataset_path = 'dataset/raw'
#
# files = [f for f in listdir(raw_dataset_path) if isfile(join(raw_dataset_path, f))]
#
# # for file in files:
