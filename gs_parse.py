from bs4 import BeautifulSoup
import requests
import parser_module
import data_module

result_list = []

def run_parse(pg, cnt):
    parser = parser_module.GS_Parse()
    for i in range(pg, pg+cnt):
        response = requests.get(f'{data_module.get_site()}/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
        flexer = BeautifulSoup(response.text, 'lxml')
        game_shit = flexer.find_all('div', {"class": "game_search"})
        for sh_elem in game_shit:
            page = requests.get(f'{data_module.get_site()}' + sh_elem.findChildren('a', recursive=False)[0]['href'])
            parser_module.print_progress(f'Страница -> {i}, игра -> {parser.get_title(page)}')
            result_list.append({
                'title': parser.get_title(page), 
                'genres': parser.get_genres(page), 
                'sys_req': parser.get_sys_req(page), 
                'same_games': parser.get_same_games(page), 
                'description': parser.get_descr(page),
                'steam_rank': parser.get_steam_rank(page),
                'metacritic_rank': parser.get_metacritic_rank(page)
                })
            # get_pic(sh_elem)

def get_result_list():
    return result_list
