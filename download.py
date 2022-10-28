import httpx
from common import read_html
from bs4 import BeautifulSoup
from anyio import open_file
from logzero import logger


async def download_file(url):
    html = await read_html(url)

    bs = BeautifulSoup(html, features='lxml')
    file_url: str = bs.find_all(class_="m-down-last")[0].a['href']
    if file_url.endswith(('.zip', '.rar')):
        await save_file(file_url)


async def save_file(url):
    client = httpx.AsyncClient()
    file_name = url.split('/')[-1]
    logger.info("{} 开始下载".format(file_name))
    async with client.stream('GET', 'https://www.example.com/') as response:
        async with await open_file('./download/{}'.format(file_name), 'wb') as f:
            async for chunk in response.aiter_bytes():
                await f.write(chunk)

    logger.info("{} 下载完毕".format(file_name))

