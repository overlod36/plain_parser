import asyncio, aiohttp
from bs4 import BeautifulSoup
import parser_module

result_list = []

def async_parse(session, index):
    pass
    # flexer = BeautifulSoup(resp, 'lxml')
    # game_shit = flexer.find_all('div', {"class": "game_search"})
    # for sh_elem in game_shit:
    #     page = session.get('https://vgtimes.ru/' + sh_elem.findChildren('a', recursive=False)[0]['href'])
    #     result_list.append({
    #         'title': parser_module.get_title(page), 
    #         'genres': parser_module.get_genres(page), 
    #         'sys_req': parser_module.get_sys_req(page), 
    #         'same_games': parser_module.get_same_games(page), 
    #         'description': parser_module.get_descr(page)
    #         })
    #     # get_pic(sh_elem)

def to_parse(pg, cnt):
    pages = []
    
        
def get_result_list():
    # обработка пустоты
    return result_list

def run_parse(pg, cnt):
    pass
    # asyncio.run(to_parse(pg, cnt))
