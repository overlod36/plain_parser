import aiohttp, asyncio
import requests

async def func():
    session = aiohttp.ClientSession()
    async with session.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/1') as resp:
        print(await resp.text())
    await session.close()
# response2 = requests.get('https://vgtimes.ru/games/release-dates/all/sort-date/alltime/page/1')
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(func())