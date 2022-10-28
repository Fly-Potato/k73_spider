import httpx


async def read_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.text
