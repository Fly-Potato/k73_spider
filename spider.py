import httpx
from bs4 import BeautifulSoup


HOST = 'http://www.k73.com'


async def loop(pages=2):
    page_num = 1
    next_url = HOST + "/down/nds/list-34-1.html"
    while page_num <= pages:
        html = await get_html(next_url)
        bs = BeautifulSoup(html, features='lxml')
        next_target = bs.find(class_="next1")
        bs = bs.find(id='download')
        for item in bs.ul.find_all(class_="item"):
            title = item.find(class_="gametitle")
            print(title.text)
        if not next_target:
            break
        try:
            next_url = HOST + next_target['href']
        except KeyError:
            break
        page_num += 1


async def get_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.text
