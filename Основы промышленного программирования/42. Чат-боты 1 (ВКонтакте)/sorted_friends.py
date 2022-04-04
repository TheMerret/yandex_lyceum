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
    resp = vk.friends.get(fields="bdate")
    if not resp["items"]:
        return
    data = ((i["first_name"], i["last_name"], i.get("bdate", "")) for i in resp["items"] if
            i.get("deactivated") is None)
    data = sorted(data, key=lambda x: x[1])
    for i in data:
        print(*i)


if __name__ == '__main__':
    main()
