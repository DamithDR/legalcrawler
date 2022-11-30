from os import listdir
from os.path import isfile, join

raw_dataset_path = 'dataset/processed_with_br'

files = [f for f in listdir(raw_dataset_path) if isfile(join(raw_dataset_path, f))]

prefixs = ['bl', 'el', 'sf', 'wl-hk', 'wl-in', 'wl-my', 'wl-nz']

counts = dict()

for prefix in prefixs:
    counts[prefix] = 0

for file in files:
    for pref in prefixs:
        if file.startswith(pref):
            counts[pref] = counts[pref] + 1

print(counts)