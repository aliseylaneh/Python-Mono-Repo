import asyncio
import random


async def task_one() -> int:
    counter = random.randint(1, 10)
    while True:
        counter += 1
        if counter >= 20:
            break
        print(f"Task One:, {counter}")
        await asyncio.sleep(0.5)
    return 20


async def task_two():
    counter = random.randint(1, 10)
    while True:
        counter += 1
        if counter >= 20:
            break
        print(f"Task Two:, {counter}")
        await asyncio.sleep(0.25)
    return 20


async def main():
    # awaitable_one = asyncio.Task(task_one())
    # awaitable_two = asyncio.Task(task_two())
    # print(type(awaitable_one))
    await asyncio.gather(*[task_one(), task_two()])
    # for coro in asyncio.as_completed([task_one(), task_two()]):
    #     value = await coro
    #     print(value)


if __name__ == "__main__":
    asyncio.run(main())
