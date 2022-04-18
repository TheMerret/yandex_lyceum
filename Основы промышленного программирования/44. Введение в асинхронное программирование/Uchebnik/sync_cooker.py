import time
from datetime import datetime


K = 1


def dish(num, prepare, wait):
    print(f"Начинаем в {datetime.now().strftime('%H:%M:%S')} "
          f"готовить блюдо № {num} будет выполнять {prepare} минут(ы)")
    time.sleep(K * prepare)
    print(f"Начинаем в {datetime.now().strftime('%H:%M:%S')} "
          f"ждать {wait} минут(ы) пока блюда № {num} приготовится")
    time.sleep(K * wait)
    print(f"Закончили в {datetime.now().strftime('%H:%M:%S')} "
          f"готовить блюдо № {num}.\n")


def main():
    dish(1, 2, 3)
    dish(2, 5, 10)
    dish(3, 3, 5)


if __name__ == '__main__':
    start_time = time.time()
    main()
    delta = int((time.time() - start_time) / K)
    print(f"Все готово в {datetime.now().strftime('%H:%M:%S')} "
          f"всего потрачено {delta}")