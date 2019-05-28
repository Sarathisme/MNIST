import pandas as pd
import os
import shutil
import inflect

number_to_word_converter = inflect.engine()


def load_data(file):
    return pd.read_csv(file)


def get_labels_and_names(data):
    labels = set(data['label'])

    structured_data = {}
    for label in labels:
        structured_data[label] = data[data['label'] == label]['filename']

    return structured_data


def create_directory_structures(labels):
    try:
        os.makedirs('data')
    except OSError as _:
        print("Directory exists!")

    try:
        os.makedirs('data/train')
        os.makedirs('data/test')
    except OSError as _:
        pass

    for label in labels:
        try:
            os.makedirs('data/train/' + str(label))
            os.makedirs('data/test/' + str(label))
        except OSError as _:
            pass


def create_validation_set():
    directory_data = {}

    for i in range(0, 10):
        for info in os.walk('data/train/%s' % str(i)):
            directory_data[str(i)] = info[2]

    for label, file in directory_data.items():
        directory_data[label] = directory_data[label][0:20]

    return directory_data


def move_files_to_validation_set(data):
    for label, files in data.items():
        for file in files:
            shutil.move('data/train/%s/%s' % (str(label), file), 'data/test/%s' % str(label))


def organize_data(data, mode='train'):
    try:
        for label, names in data.items():
            for name in names:
                shutil.move('Train_Data/Images/%s/%s' % (mode, name), 'data/%s/%s' % (mode, str(label)))
    except OSError as _:
        pass


if __name__ == "__main__":
    raw_data = load_data('Train_Data/train.csv')
    filtered_data = get_labels_and_names(raw_data)
    create_directory_structures(filtered_data.keys())
    organize_data(filtered_data, mode='train')
    move_files_to_validation_set(create_validation_set())