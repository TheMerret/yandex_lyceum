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

    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_wall(["serzh.jpg"])
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    vk = vk_session.get_api()
    vk.wall.post(message="Сергей?", attachments=[vk_photo_id])


if __name__ == '__main__':
    main()
