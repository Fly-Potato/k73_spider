import asyncio

import httpx
from bs4 import BeautifulSoup

from common import read_html
from download import download_file
from logzero import logger


HOST = 'http://www.k73.com'


async def loop(pages=3):
    page_num = 1
    next_url = HOST + "/down/nds/list-34-1.html"
    while page_num <= pages:
        html = await read_html(next_url)
        bs = BeautifulSoup(html, features='lxml')
        next_target = bs.find(class_="next1")
        bs = bs.find(id='download')
        tasks = []
        for item in bs.ul.find_all(class_="item"):
            title = item.find(class_="gametitle")
            logger.info(title.text.strip())
            logger.info(item.find(class_="ngamename").p.contents[1].text)
            go_down = item.find(class_='go_down')
            if go_down:
                tasks.append(download_file(HOST + go_down['href']))
        await asyncio.gather(*tasks)
        if not next_target:
            break
        try:
            next_url = HOST + next_target['href']
        except KeyError:
            break
        page_num += 1

