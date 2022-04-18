import asyncio
import time
from datetime import datetime


K = 1


async def dish(num, prepare, wait):
    print(f"Начинаем в {datetime.now().strftime('%H:%M:%S')} "
          f"готовить блюдо № {num} будет выполнять {prepare} минут(ы)")
    time.sleep(K * prepare)  # синхронно т.к повар занят
    print(f"Начинаем в {datetime.now().strftime('%H:%M:%S')} "
          f"ждать {wait} минут(ы) пока блюда № {num} приготовится")
    await asyncio.sleep(K * wait)  # асинхронный вызов
    print(f"Закончили в {datetime.now().strftime('%H:%M:%S')} "
          f"готовить блюдо № {num}.\n")


async def main():
    coros = dish(1, 2, 3), dish(2, 5, 10), dish(3, 3, 5)
    await asyncio.gather(*(asyncio.create_task(coro) for coro in coros))


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    delta = int((time.time() - start_time) / K)
    print(f"Все готово в {datetime.now().strftime('%H:%M:%S')} "
          f"всего потрачено {delta}")