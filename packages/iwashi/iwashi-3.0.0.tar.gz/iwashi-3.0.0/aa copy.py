import asyncio
import aiohttp
from iwashi.helper import print_result
from iwashi.iwashi import visit

session = aiohttp.ClientSession()


async def main():
    result = await visit("https://youtu.be/_fC09zQyejI")
    if result:
        print_result(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
