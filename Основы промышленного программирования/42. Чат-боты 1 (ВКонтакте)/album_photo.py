import os

import vk_api

from login_password import LOGIN, PASSWORD


ALBUM_ID = os.getenv("ALBUM_ID")
GROUP_ID = os.getenv("GROUP_ID")


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return error_msg
    vk = vk_session.get_api()
    photos = vk.photos.get(group_id=GROUP_ID, album_id=ALBUM_ID)
    photos = photos["items"]
    for photo in photos:
        max_photo = photo["sizes"][-1]
        print("URI:", max_photo["url"])
        print("SIZE:", f"{max_photo['width']}x{max_photo['height']}")
        print()


if __name__ == '__main__':
    main()