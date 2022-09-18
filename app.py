import requests
from bs4 import BeautifulSoup

for i in range(1, 2663):
    response = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
    flexer = BeautifulSoup(response.text, 'lxml')
    game_shit = flexer.find_all('div', {"class": "game_search"})

    for sh_elem in game_shit:
        print(sh_elem.findChildren('a', recursive=False)[0]['title'].replace(' - дата выхода', ''))
    