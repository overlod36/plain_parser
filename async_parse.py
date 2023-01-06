import asyncio, aiohttp
from bs4 import BeautifulSoup
import parser_module
import requests

result_list = []

async def async_parse(session, index):
    async with session.get(f'https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/{index}') as resp:
        text = await resp.text()
        flexer = BeautifulSoup(text, 'lxml') #?
        game_shit = flexer.find_all('div', {"class": "game_search"})
        for sh_elem in game_shit:
            page = requests.get('https://vgtimes.ru/' + sh_elem.findChildren('a', recursive=False)[0]['href'])
            result_list.append({
                'title': parser_module.get_title(page), 
                'genres': parser_module.get_genres(page), 
                'sys_req': parser_module.get_sys_req(page), 
                'same_games': parser_module.get_same_games(page), 
                'description': parser_module.get_descr(page)
                })
            # get_pic(sh_elem)

async def to_parse(pg, cnt):
    session = aiohttp.ClientSession()
    pages = set()
    async with session.get(f'https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/') as resp:
        for i in range(pg, pg+cnt):
            task = asyncio.create_task(async_parse(session, i))
            pages.add(task)
        await asyncio.gather(*pages)
        await session.close()
    



    
        
def get_result_list():
    # обработка пустоты
    return result_list

def run_parse(pg, cnt):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(to_parse(pg, cnt))
