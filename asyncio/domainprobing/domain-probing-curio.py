from curio import run, TaskGroup
import curio.socket as socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> tuple[str, bool]:
    try:
        await socket.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, False)


async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.dev" for name in names)
    async with TaskGroup() as group:
        for domain in domains:
            await group.spawn(probe, domain)
        async for task in group:
            domain, found = task.result
            mark = "+" if found else ""
            print(f"{mark} {domain}")


if __name__ == "__main__":
    run(main())
