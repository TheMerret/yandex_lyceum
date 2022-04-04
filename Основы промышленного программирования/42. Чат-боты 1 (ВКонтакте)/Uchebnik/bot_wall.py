from pprint import pprint

import vk_api
from login_password import LOGIN, PASSWORD


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.VkApiError as e:
        print(e)
        return
    print("Авторизация успешна!")
    vk = vk_session.get_api()
    resp = vk.wall.get(count=0, offset=0)
    if resp["items"]:
        for i in resp["items"]:
            pprint(i)


if __name__ == '__main__':
    main()