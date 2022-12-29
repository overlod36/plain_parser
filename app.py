from reprlib import recursive_repr
from urllib import response
import requests
from bs4 import BeautifulSoup
import sqlite3


def create_db_table(db):
    sql_cr = db.cursor()
    sql_cr.execute("""CREATE TABLE IF NOT EXISTS games(
    g_id INTEGER PRIMARY KEY,
    g_title TEXT NOT NULL,
    release_date TEXT,
    system_req TEXT,
    g_description TEXT,
    g_genres TEXT,
    same_g TEXT
    )""")

def add_game(elems, db):
    db.execute(f"INSERT INTO games(g_title, release_date, system_req, g_description, g_genres, same_g) VALUES (?,?,?,?,?,?)", (elems[0], elems[5][0], conv_to_str(elems[2]), elems[4], conv_to_str(elems[1]), conv_to_str(elems[3])))
    db.commit()

def show_games(db):
    sd = db.cursor()
    print(list(sd.execute("SELECT * FROM games")))

def conv_to_str(lst):
    st = ""
    for el in lst:
        st = el + '|'
    return st[:len(st)-1] 

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
    return BeautifulSoup(pg.text, 'lxml').find('div', {'class': 'game_header'}).findChildren('h1', recursive=False)[0].text

def get_genres(pg):
    return [el.text for el in BeautifulSoup(pg.text, 'lxml').find_all('div', {'class': 'gres'})[0].findChildren('a', recursive=False)]

def get_sys_req(pg):
    if check_for_text('Системные требования', BeautifulSoup(pg.text, 'lxml').find('div', {'class':'wrap ld'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)):
        return [tt.text for tt in (BeautifulSoup(pg.text, 'lxml').find('h2', {'class':'nhead'}, string='Системные требования').next_sibling.next_sibling.next_sibling.next_sibling.findChildren('li', recursive=False))]
    return []

def get_same_games(pg):
    if check_for_text('Похожие игры', BeautifulSoup(pg.text, 'lxml').find('div', {'class':'wrap ld'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)):
        return [sg.text for sg in (BeautifulSoup(pg.text, 'lxml').find('h2', {'class':'nhead'}, string='Похожие игры').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.findChildren('li', recursive=False))]
    return []

def get_descr(pg):
    print(BeautifulSoup(pg.text, 'lxml').find('div', {'class':'game_story description'}).findChildren('p', recursive=False))
    return BeautifulSoup(pg.text, 'lxml').find('div', {'class':'game_story description'}).findChildren('p', recursive=False)[0].text

def get_another(pg):
    elems = BeautifulSoup(pg.text, 'lxml').find_all('div', {'class': 'rads'})
    if elems[0].findChildren('div', {'class': 'game_rank'}):
        return [elems[1].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text, elems[2].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text]
    else:
        return [elems[0].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text, elems[1].findChildren('div', recursive=False)[0].findChildren('a', recursive=False)[0].text]


def get_all(db):
    prep_fl = BeautifulSoup(requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/').text, 'lxml')
    pages_div = prep_fl.find('div', {'class':'pages'}).findChildren('div', recursive=False)[0].find_all('a')
    pages_count = int(pages_div[len(pages_div)-2].text) + 1
    for i in range(100, pages_count):
        response = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
        flexer = BeautifulSoup(response.text, 'lxml')
        game_shit = flexer.find_all('div', {"class": "game_search"})

        for sh_elem in game_shit:
            page = requests.get('https://vgtimes.ru/' + sh_elem.findChildren('a', recursive=False)[0]['href'])
            res = [get_title(page), get_genres(page), get_sys_req(page), get_same_games(page), get_descr(page), get_another(page)]
            #add_game(res, db)
            print(res)
            
        break
    #show_games(db)
            

if __name__ == '__main__':
    db = sqlite3.connect('games.db')
    create_db_table(db)
    get_all(db)
