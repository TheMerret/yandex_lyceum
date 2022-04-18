import logging
import os

import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater, MessageHandler, Filters, CallbackContext, CommandHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

URL = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
API_KEY = os.getenv("API_KEY")
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}


def start(update: Update, context: CallbackContext):
    logger.info("dialog started")
    context.user_data["frm"] = "ru"
    context.user_data["to"] = "en"
    frm, to = context.user_data["frm"], context.user_data["to"]
    translation_keyboard = [[f"/change {to} {frm}"]]
    reply_keyboard = ReplyKeyboardMarkup(translation_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите слово, и я его переведу.", reply_markup=reply_keyboard)


def translate_api(text, lang_from="ru", lang_to="en"):
    params = {
        "langpair": f"{lang_from}|{lang_to}",
        "q": text,
    }

    resp = requests.get(URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    resp_json = resp.json()
    status_code = resp_json["responseStatus"]
    status_code = 200 if status_code is None else int(status_code)
    resp.status_code = status_code
    reason = resp_json["responseDetails"]
    resp.reason = reason
    resp.raise_for_status()
    response_data = resp_json["responseData"]
    translation = response_data["translatedText"]
    return translation


def translate(update: Update, context: CallbackContext):
    text = update.message.text
    frm, to = context.user_data["frm"], context.user_data["to"]
    print(frm, to)
    translation_keyboard = [[f"/change {to} {frm}"]]
    reply_keyboard = ReplyKeyboardMarkup(translation_keyboard)
    try:
        res = translate_api(text, frm, to)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{res}", reply_markup=reply_keyboard)
    except requests.HTTPError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Ошибка перевода. {e}", reply_markup=reply_keyboard)


def change_direction(update: Update, context: CallbackContext):
    try:
        frm, to = context.args
        context.user_data["frm"] = frm
        context.user_data["to"] = to
        translation_keyboard = [[f"/change {to} {frm}"]]
        reply_keyboard = ReplyKeyboardMarkup(translation_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Теперь направление: {frm} -> {to}',
                                 reply_markup=reply_keyboard)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Использование: /change en ru")


def stop(update, context):
    update.message.reply_text("Всего хорошего")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("change", change_direction))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
