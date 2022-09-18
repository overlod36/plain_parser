import requests
from bs4 import BeautifulSoup

for i in range(1, 2663):
    response = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
    flexer = BeautifulSoup(response.text, 'lxml')
    game_shit = flexer.find_all('div', {"class": "game_search"})

    for sh_elem in game_shit:
        game_name = sh_elem.findChildren('a', recursive=False)[0]
        #print(game_name['title'].replace(' - дата выхода', ''))
        game_resp = requests.get('https://vgtimes.ru/' + game_name['href'])
        g_html = BeautifulSoup(game_resp.text, 'lxml')
        main_el = g_html.find('div', {'class': 'game_header'})
        print(main_el.findChildren('h1', recursive=False)[0].text)
    