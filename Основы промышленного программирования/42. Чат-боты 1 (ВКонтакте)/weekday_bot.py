import logging
import os
import random
import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

datastore = {}  # user_id: 1/0 (новое сообщение или нет)


def handle_message(vk, event):
    logger.info(event)
    logger.info('Новое сообщение:')
    user_id = event.obj.message['from_id']
    logger.info('Для меня от: %s', user_id)
    text = event.obj.message['text']
    logger.info('Текст: %s', text)
    if not datastore.get(user_id):
        datastore[user_id] = 1
        msg = "Введите дату в формате YYYY-MM-DD, и я скажу в какой день недели это было."
    else:
        try:
            date_text = datetime.datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            msg = "Неверный формат. Пример даты: 1980-01-31"
        else:
            weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота",
                        "Воскресенье"]
            weekday = weekdays[date_text.weekday()]
            msg = weekday
    vk.messages.send(user_id=user_id,
                     message=msg,
                     random_id=random.randint(0, 2 ** 64))


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
