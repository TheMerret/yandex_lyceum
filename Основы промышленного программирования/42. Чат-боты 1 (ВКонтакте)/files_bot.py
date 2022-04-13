import os

import vk_api
from vk_api.upload import VkUpload

from login_password import LOGIN, PASSWORD


ALBUM_ID = 000000000
GROUP_ID = 000000000


def get_photos():
    base_dir = "static/img"
    photo_paths = [os.path.join(base_dir, i) for i in os.listdir(base_dir)]
    return photo_paths


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return error_msg
    upload = VkUpload(vk_session)
    photos = get_photos()
    upload.photo(photos, ALBUM_ID, group_id=GROUP_ID)


if __name__ == '__main__':
    main()