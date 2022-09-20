from reprlib import recursive_repr
from urllib import response
import requests
from bs4 import BeautifulSoup

def get_pic_name(url):
    lt = url.split('/')
    return lt[len(lt) - 1]

def check_for_text(txt, html):
    for el in html:
        if el.text == txt:
            return True
    return False

def get_pic(div):
    url = div.findChildren('a', recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('img', recursive=False)[0]['src']
    if url != '/img/no_game_img_mini.jpg':
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

def get_info(pg):
    g_html = BeautifulSoup(pg.text, 'lxml')
    elems = g_html.find_all('div', {'class': 'rads'})
    descr = g_html.find('div', {'class':'game_story description'})
    genres = g_html.find_all('div', {'class': 'gres'})[0].findChildren('a', recursive=False)
    ch_req = g_html.find('div', {'class':'wrap ld'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)
    print('Дата выхода:', end=' ')
    if elems[0].findChildren('div', {'class': 'game_rank'}):
        print(elems[1].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text) #дата выхода
        print('Команда разработчиков:', end=' ')
        print(elems[2].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text) #разработчик
    else:
        print(elems[0].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text) #дата выхода
        print('Команда разработчиков:', end=' ')
        print(elems[1].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text) #разработчик
    print('Описание игры:')
    print(descr.findChildren('p', recursive=False)[0].text)
    print('Жанры:')
    for el in genres:
        print(el.text)
    if check_for_text('Системные требования', ch_req):
        req = g_html.find('h2', {'class':'nhead'}, string='Системные требования')
        print('Системные требования:')
        for tt in (req.next_sibling.next_sibling.next_sibling.next_sibling.findChildren('li', recursive=False)):
            print(tt.text)
    


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
            print('Название игры:', end=' ')
            get_title(page)
            get_info(page)
            get_pic(sh_elem)
            break
        break

if __name__ == '__main__':
    get_all()
