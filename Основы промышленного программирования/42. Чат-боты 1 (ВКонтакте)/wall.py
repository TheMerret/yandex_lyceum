from datetime import datetime

import vk_api
from login_password import LOGIN, PASSWORD


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.VkApiError as e:
        print(e)
        return
    vk = vk_session.get_api()
    resp = vk.wall.get(count=5, offset=0)
    if not resp["items"]:
        return
    for i in resp["items"]:
        print(i["text"] + ";")
        date = datetime.fromtimestamp(i["date"])
        print(f"date: {date.date().isoformat()}", f"time: {date.time().isoformat()}", sep=", ", end="\n\n")


if __name__ == '__main__':
    main()