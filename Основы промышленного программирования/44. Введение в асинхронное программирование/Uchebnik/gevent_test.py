import gevent.monkey
from urllib.request import urlopen


gevent.monkey.patch_all()

urls = [
    "https://google.com",
    "https://yandex.ru",
    "https://python.org"
]


def print_head(url):
    print(f"Старт {url}")
    data = urlopen(url).read(100)
    print(f"{url}: {len(data)} данные: {data} ...")


jobs = [gevent.spawn(print_head, url) for url in urls]
gevent.wait(jobs)