import aiohttp
import requests
# session = aiohttp.ClientSession()
# response1 = session.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/1')
response2 = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/1')
# print(response1)
print(response2)