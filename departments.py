from os import listdir
import json


def create_departments():
    text_files = "./resources/ETD_metadata"
    dept_line = 4
    data = {}
    for file in listdir(text_files):
        with open(text_files + '/' + file, 'r', encoding='utf-8') as text_file:
            for i, line in enumerate(text_file.readlines()):
                line = line.replace("\n", "")
                if i == dept_line:
                    if line not in data:
                        data[line] = [file]
                    else:
                        data[line].append(file)
                    break
    with open('./resources/departments.json', 'w') as json_file:
        json.dump(data, json_file)


def get_departments():
    with open('./resources/departments.json', 'r') as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    create_departments()
