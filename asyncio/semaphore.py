import asyncio
import aiohttp


async def fetch_data(
    session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore
):
    async with semaphore:
        async with session.get(url=url) as response:
            data = await response.json()
            print(f"Recieved data from {url}: {data}")


async def main():
    semaphore = asyncio.Semaphore(2)
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://www.fluentpython.com/data/flags/CN/CN.gif",
            "https://www.fluentpython.com/data/flags/IN/IN.gif",
            "https://www.fluentpython.com/data/flags/US/US.gif",
        ]
        tasks = [
            fetch_data(session=session, url=url.lower(), semaphore=semaphore)
            for url in urls
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
