from reprlib import recursive_repr
from urllib import response
import requests
import data_module
from bs4 import BeautifulSoup
import os, sys

for_pr = False

def print_progress(message):
    global for_pr
    if for_pr:
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        print(message)
    else:
        print(message)
        for_pr = True


def conv_to_str(lst):
    st = ""
    for el in lst:
        st = el + '|'
    return st[:len(st)-1]

class GS_Parse:

    def get_pic_name(self, url):
        lt = url.split('/')
        return lt[len(lt) - 1]

    def check_for_text(self, txt, html):
        for el in html:
            if el.text == txt:
                return True
        return False

    def get_pic(self, div):
        url = div.findChildren('a', recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('img', recursive=False)[0]['src']
        if url != '/img/no_game_img_mini.jpg':
            with open('img/' + self.get_pic_name(url), 'wb') as st:
                response = requests.get(f'{data_module.get_site()}{url}', stream=True)

                for block in response.iter_content(1024):
                    if not block:
                        break
                    st.write(block)

    def get_title(self, pg):
        return BeautifulSoup(pg.text, 'lxml').find('div', {'class': 'game_header'}).findChildren('h1', recursive=False)[0].text

    def get_genres(self, pg):
        return [el.text for el in BeautifulSoup(pg.text, 'lxml').find_all('div', {'class': 'gres'})[0].findChildren('a', recursive=False)]

    def get_sys_req(self, pg):
        if self.check_for_text('Системные требования', BeautifulSoup(pg.text, 'lxml').find('div', {'class':'wrap ld'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)):
            li_list = BeautifulSoup(pg.text, 'lxml').find('h2', {'class':'nhead'}, string='Системные требования').parent.parent.find('div', {'class':'article_block a_list'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)
            return [tt.text for tt in li_list]
        return []

    def get_same_games(self, pg):
        if self.check_for_text('Похожие игры', BeautifulSoup(pg.text, 'lxml').find('div', {'class':'wrap ld'}).findChildren('ul', recursive=False)[0].findChildren('li', recursive=False)):
            return [sg.text for sg in (BeautifulSoup(pg.text, 'lxml').find('h2', {'class':'nhead'}, string='Похожие игры').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.findChildren('li', recursive=False))]
        return []

    def get_descr(self, pg):
        descr_html = BeautifulSoup(pg.text, 'lxml').find('div', {'class':'game_story description'})
        if len(descr_html) != 0 and len(descr_html.findChildren('p', recursive=False)) != 0: 
            return descr_html.findChildren('p', recursive=False)[0].text
        else:
            return []

    def get_steam_rank(self, pg):
        steam_html = BeautifulSoup(pg.text, 'lxml').find_all('div', {'class':'game_rank steam'})
        if len(steam_html) != 0:
            return steam_html[0].findChildren('div', {'class':'score'})[0].text.split('/')[0]
        else:
            return []
        
    def get_metacritic_rank(self, pg):
        meta_html = BeautifulSoup(pg.text, 'lxml').find_all('div', {'class':'game_rank mc'})
        if len(meta_html) != 0:
            return meta_html[0].findChildren('div', {'class':'score'})[0].text.split('/')[0]
        else:
            return []


    def get_pages_count():
        prep_fl = BeautifulSoup(requests.get(f'{data_module.get_site()}/games/release-dates/all/sort-date/alltime/').text, 'lxml')
        pages_div = prep_fl.find('div', {'class':'pages'}).findChildren('div', recursive=False)[0].find_all('a')
        pages_count = int(pages_div[len(pages_div)-2].text) + 1
        return pages_count

