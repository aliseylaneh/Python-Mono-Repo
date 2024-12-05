import asyncio

import random


async def async_generator():
    for i in range(5):
        await asyncio.sleep(random.randint(1, 4))
        yield i


async def main():
    async for i in async_generator():
        print(i)


if __name__ == "__main__":
    asyncio.run(main())
