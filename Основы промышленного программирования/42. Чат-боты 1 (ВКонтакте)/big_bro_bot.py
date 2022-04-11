import logging
import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    vk = vk_session.get_api()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
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
            if city := user.get("city"):
                city = city["title"]
                message = f"Как поживает {city}?"
                vk.messages.send(user_id=user_id,
                                 message=message,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
