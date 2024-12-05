import asyncio

from contextlib import asynccontextmanager
import requests


def download_page(url: str):
    data = requests.get(url=url)
    data.raise_for_status()
    return data


def update_stats(url: str):
    print(f"Request for {url} is done")


@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(None, download_page, url)
    yield data
    await loop.run_in_executor(None, update_stats, url)


def process(page: requests):
    print("page resolved")


async def main():
    async with web_page("https://www.google.com") as page:
        process(page)
        print("NOT EXITED YET")
    print("EXISTED")


if __name__ == "__main__":
    asyncio.run(main())
