import logging
import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from login_password import LOGIN, PASSWORD
import random

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ALBUM_ID = os.getenv("ALBUM_ID")


def get_photo():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        logger.error(error_msg)
        raise
    vk = vk_session.get_api()
    photos = vk.photos.get(group_id=CLUB_ID, album_id=ALBUM_ID)
    photos = photos["items"]
    photo = random.choice(photos)
    photo_id = f"photo{photo['owner_id']}_{photo['id']}"
    return photo_id


def handle_message(vk, event):
    logger.info(event)
    logger.info('Новое сообщение:')
    user_id = event.obj.message['from_id']
    logger.info('Для меня от: %s', user_id)
    logger.info('Текст: %s', event.obj.message['text'])
    user = vk.users.get(user_id=user_id, fields="city")[0]
    message = f"Привет, {user['first_name']}!"
    vk.messages.send(user_id=user_id,
                     message=message,
                     random_id=random.randint(0, 2 ** 64))
    photo_id = get_photo()
    vk.messages.send(user_id=user_id,
                     message="Фоточка)",
                     random_id=random.randint(0, 2 ** 64),
                     attachment=photo_id)


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    vk = vk_session.get_api()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(vk, event)


if __name__ == '__main__':
    main()
