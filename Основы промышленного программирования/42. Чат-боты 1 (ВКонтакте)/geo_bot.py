import logging
import os
import random
from io import BytesIO
from collections import defaultdict
import json

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api import VkUpload

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# user_id: {"user_activated": 0, "keyboard_activated": 0, "tponym": toponym}
datastore = defaultdict(dict)


def get_geocode_result(geocode_data, **params):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode_data,
        "format": "json",
        **params
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()

    return json_response


def get_toponym(geocode_result):
    # Получаем первый топоним из ответа геокодера.
    try:
        toponym = geocode_result["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
    except (KeyError, IndexError):
        raise ValueError
    return toponym


def get_address_bbox(toponym):
    envelope = toponym['boundedBy']['Envelope']
    bbox = f"{envelope['lowerCorner']}~{envelope['upperCorner']}".replace(" ", ",")
    return bbox


def get_ll_from_geocode_response(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return toponym_longitude, toponym_lattitude


def get_static_map_url(lat=None, lon=None, **params):
    # Собираем параметры для запроса к StaticMapsAPI:
    map_type = params.get('l', 'map')
    map_params = {
        'l': map_type,
        **params,
    }
    if not (lat is None or lon is None):
        ll = ",".join([lat, lon])
        map_params['ll'] = ll
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    url = requests.Request(url=map_api_server, params=map_params).prepare().url
    return url


def handle_message(vk, event):
    logger.info(event)
    logger.info('Новое сообщение:')
    user_id = event.obj.message['from_id']
    logger.info('Для меня от: %s', user_id)
    text = event.obj.message['text']
    logger.info('Текст: %s', text)
    if not datastore[user_id].get("user_activated"):
        datastore[user_id]["user_activated"] = 1
        datastore[user_id]["keyboard_activated"] = 0
        msg = "Скажити название местности, я покажу это на карте."
        vk.messages.send(user_id=user_id,
                         message=msg,
                         random_id=random.randint(0, 2 ** 64))
        return
    geocode_result = get_geocode_result(text)
    if not datastore[user_id]["keyboard_activated"]:
        try:
            toponym = get_toponym(geocode_result)
            datastore[user_id]["toponym"] = toponym
        except ValueError:
            logger.error("not found")
            msg = "Ничего не найдено. Скорее всего запрос набран с ошибкой"
            vk.messages.send(user_id=user_id,
                             message=msg,
                             random_id=random.randint(0, 2 ** 64))
            return
        datastore[user_id]["keyboard_activated"] = 1
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Схема", payload={"map_type": "map"})
        keyboard.add_button("Спутник", payload={"map_type": "sat"})
        keyboard.add_button("Гибрид", payload={"map_type": "sat,skl"})
        vk.messages.send(user_id=user_id,
                         message="Выберете тип карты:",
                         keyboard=keyboard.get_keyboard(),
                         random_id=random.randint(0, 2 ** 64))
        return
    datastore[user_id]["keyboard_activated"] = 0
    toponym = datastore[user_id]["toponym"]
    bbox = get_address_bbox(toponym)
    coord = get_ll_from_geocode_response(toponym)
    pointer = f"{coord[0]},{coord[1]},pm2rdl"
    kb_payload = event.message.payload
    kb_payload = json.loads(kb_payload)
    map_type = kb_payload["map_type"]
    url = get_static_map_url(bbox=bbox, pt=pointer, l=map_type)
    static_map = requests.get(url).content
    geocode_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    logger.info("found image")
    upload = VkUpload(vk)
    message_peer_id = random.randint(0, 2 ** 64)
    msg = f" Это {geocode_address}. Что вы еще хотите увидеть?"
    photo = upload.photo_messages(BytesIO(static_map))
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(user_id=user_id,
                     message=msg,
                     random_id=message_peer_id, attachment=attachment)


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    vk = vk_session.get_api()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(vk, event)
        print(event)


if __name__ == '__main__':
    main()
