import logging
import os

import requests
from telegram import Update
from telegram.ext import (Updater, MessageHandler, Filters, CallbackContext, CommandHandler)
from telegram.error import NetworkError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")


def start(update: Update, context: CallbackContext):
    logger.info("dialog started")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите название объекта, и я покажу его на карте.")


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


def geocode(update: Update, context: CallbackContext):
    geocode_result = get_geocode_result(update.message.text)
    try:
        toponym = get_toponym(geocode_result)
    except ValueError:
        logger.error("not found")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ничего не найдено. Скорее всего запрос набран с ошибкой")
        return
    bbox = get_address_bbox(toponym)
    coord = get_ll_from_geocode_response(toponym)
    pointer = f"{coord[0]},{coord[1]},pm2rdl"
    url = get_static_map_url(bbox=bbox, pt=pointer)
    geocode_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    logger.info("found image")
    try:
        context.bot.send_photo(update.message.chat_id, url, caption=geocode_address)
    except NetworkError as e:
        logger.error(f"{e.__class__.__name__} {e.message}")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Ошибка на сервере карт: {e.__class__.__name__} {e.message}")


def stop(update, context):
    update.message.reply_text("Всего хорошего")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, geocode))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
