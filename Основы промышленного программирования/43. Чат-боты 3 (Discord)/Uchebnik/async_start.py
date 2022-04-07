import asyncio


async def work(name):
    print(f"{name} началась")
    await asyncio.sleep(5)
    print(f"{name} завершилась")


async def main():
    await asyncio.gather(
        asyncio.create_task(work("Первая")),
        asyncio.create_task(work("Вторая")),
    )


if __name__ == '__main__':
    asyncio.run(main())