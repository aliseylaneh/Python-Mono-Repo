import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional

from keyword import kwlist

MAX_KEYWORD_LEN = 4


class Result(NamedTuple):  # <1>
    domain: str
    found: bool


OptionalLoop = Optional[asyncio.AbstractEventLoop]  # <2>


async def probe(domain: str, loop: OptionalLoop = None) -> Result:  # <3>
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:  # <4>
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]  # <5>
    for coro in asyncio.as_completed(coros):  # <6>
        result = await coro  # <7>
        yield result  # <8>


async def main():
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.dev".lower() for name in names)
    async for result in multi_probe(domains=domains):
        domain, found = result
        mark = "+" if found else ""
        print(f"{mark} {domain}")


if __name__ == "__main__":
    asyncio.run(main())
