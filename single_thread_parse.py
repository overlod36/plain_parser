from bs4 import BeautifulSoup
import requests
import parser_module

result_list = []

def run_parse(pg, cnt):
    for i in range(pg, pg+cnt):
        response = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/' + str(i) + '/')
        flexer = BeautifulSoup(response.text, 'lxml')
        game_shit = flexer.find_all('div', {"class": "game_search"})
        for sh_elem in game_shit:
            page = requests.get('https://vgtimes.ru/' + sh_elem.findChildren('a', recursive=False)[0]['href'])
            parser_module.print_progress(f'Страница -> {i}, игра -> {parser_module.get_title(page)}')
            parser_module.get_steam_rank(page)
            result_list.append({
                'title': parser_module.get_title(page), 
                'genres': parser_module.get_genres(page), 
                'sys_req': parser_module.get_sys_req(page), 
                'same_games': parser_module.get_same_games(page), 
                'description': parser_module.get_descr(page),
                'steam_rank': parser_module.get_steam_rank(page),
                'metacritic_rank': parser_module.get_metacritic_rank(page)
                })
            # get_pic(sh_elem)

def get_result_list():
    return result_list
