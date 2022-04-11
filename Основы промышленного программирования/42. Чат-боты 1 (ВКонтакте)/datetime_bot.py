import datetime
import logging
import os
import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handle_message(vk, event):
    logger.info(event)
    logger.info('Новое сообщение:')
    user_id = event.obj.message['from_id']
    logger.info('Для меня от: %s', user_id)
    text = event.obj.message['text']
    logger.info('Текст: %s', text)
    markers = ["время", "число", "дата", "день"]
    if any(i in text for i in markers):
        # москва
        datetime_res = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вск"]
        msg = f"Дата: {datetime_res.date().isoformat()}\n" \
              f"Московское время: {datetime_res.time().isoformat()}\n" \
              f"День недели {weekdays[datetime_res.weekday()]}"
    else:
        msg = """Вы можете попросить меня вывести текущую дату, время, день недели"""
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
