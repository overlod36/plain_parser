from reprlib import recursive_repr
from urllib import response
import requests
from bs4 import BeautifulSoup

def get_pic_name(url):
    lt = url.split('/')
    return lt[len(lt) - 1]

def get_pic(div):
    url = div.findChildren('a', recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('img', recursive=False)[0]['src']
    with open('img/' + get_pic_name(url), 'wb') as st:
        response = requests.get('https://vgtimes.ru' + url, stream=True)

        for block in response.iter_content(1024):
            if not block:
                break

            st.write(block)

def get_title(pg):
    g_html = BeautifulSoup(pg.text, 'lxml')
    main_el = g_html.find('div', {'class': 'game_header'})
    print(main_el.findChildren('h1', recursive=False)[0].text)

def get_all():
    prep_fl = BeautifulSoup(requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/').text, 'lxml')
    pages_div = prep_fl.find('div', {'class':'pages'}).findChildren('div', recursive=False)[0].find_all('a')
    pages_count = int(pages_div[len(pages_div)-2].text) + 1
    for i in range(1, pages_count):
        response = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
        flexer = BeautifulSoup(response.text, 'lxml')
        game_shit = flexer.find_all('div', {"class": "game_search"})

        for sh_elem in game_shit:
            page = requests.get('https://vgtimes.ru/' + sh_elem.findChildren('a', recursive=False)[0]['href'])
            get_title(page)
            get_pic(sh_elem)

if __name__ == '__main__':
    get_all()
