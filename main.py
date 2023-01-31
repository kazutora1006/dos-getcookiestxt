import json
import aiohttp
import asyncio

from makerdpost import RandomData

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

rd = RandomData()


async def main():
    async with aiohttp.ClientSession() as session:
        i = 1
        while True:
            data = rd()
            async with session.post("https://ck.getcookiestxt.com/getcookie", headers=data.headers, json=data.data) as res:
                t = await res.text()
                if not res.ok:
                    print(t)
                    break
                else:
                    print(str(i).zfill(8),res.status,t)
                    i += 1

asyncio.run(main())
