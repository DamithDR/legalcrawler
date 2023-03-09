import json
import os

from sklearn.model_selection import train_test_split

dataset_path = 'dataset/processed_without_br/filtered/deduplicated'

files = os.listdir(dataset_path)

train, test = train_test_split(files, test_size=200, random_state=777)

train_list = []
for file in train:
    path = dataset_path + '/' + file
    with open(path, 'r') as f:
        content = f.read()
        train_contents_dict = {'case_number': file, 'text': content}
        train_list.append(train_contents_dict)

test_list = []
for file in test:
    path = dataset_path + '/' + file
    with open(path, 'r') as f:
        content = f.read()
        test_contents_dict = {'case_number': file, 'text': content}
        test_list.append(test_contents_dict)

final_dataset_path = 'dataset/final/'
with open(final_dataset_path + 'train.json', 'w') as jf:
    json.dump(train_list, jf)
with open(final_dataset_path + 'test.json', 'w') as jf:
    json.dump(test_list, jf)
