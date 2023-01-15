import json
from datetime import datetime
import pathlib, os

pt = pathlib.Path(__file__).parent.resolve() # спуститься вниз после перемещения модуля

def write_journal(data, info):
    with open(f'{pt}/journals/{info}{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json', 'w', encoding='utf-8') as outf:
        json.dump(data, outf, ensure_ascii=False, indent=4)

def print_journal_list(): # изменить вывод с учетом разных подпапок
    for file in os.listdir(f'{pt}/journals'):
        if file.endswith('.json'):
            print(file)

def get_site():
    with open(f'{pt}/config/site_name.txt', 'r') as file:
        return file.readline()

