import asyncio
import aiohttp
from iwashi.visitors.youtube import Youtube

session = aiohttp.ClientSession()


async def main():
    result = await Youtube().visit_url(
        session, "https://youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
    )
    print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
