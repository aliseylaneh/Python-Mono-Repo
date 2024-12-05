from httpx import AsyncClient
import asyncio
from pathlib import Path
from typing import Callable
import time

POP20_CC = ("CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR").split()
BASE_URL = "https://www.fluentpython.com/data/flags"
DEST_DIR = Path("downloaded")


# Base functionality
async def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)


async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    response = await client.get(url, timeout=6.1, follow_redirects=True)
    response.raise_for_status()
    return response.read()  # Network I/O operatrions are implemented as coroutine methods, so they are driven asyn by asyncio event loop.


async def download_one(client: AsyncClient, cc: str):
    image = await get_flag(client=client, cc=cc)
    asyncio.as_completed([save_flag(image, f"{cc}.gif")])
    print(cc, end=" | ", flush=True)
    return cc


def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list))


async def supervisor(cc_list: list[str]):
    """
    Asynchronous HTTP client operations in httpx are methods of AsyncClient,
    which is also an asynchronous context manager: a context manager with asyn‐
    chronous setup and teardown methods
    """
    async with AsyncClient() as client:  # Open a httpx async client connection
        to_do = [
            download_one(client, cc) for cc in sorted(cc_list)
        ]  # create a list of coroutines of download_one() coroutine
        res = await asyncio.gather(
            *to_do
        )  # gathering task and scheduling them to run / wait and expects the reponse
    return len(res)


def main(downloader: Callable[[list[str]], int]) -> None:
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f"\n{count} downloads in {elapsed:.2f}s")


if __name__ == "__main__":
    main(download_many)
