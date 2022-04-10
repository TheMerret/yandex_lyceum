import logging
import os
import json
import random

from telegram import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")


with open(input("Введите имя файла: "), "r", encoding="utf8") as fd:
    test_data = json.load(fd)
    test_data = test_data["test"]


def start(update: Update, context: CallbackContext):
    test_data[:] = random.sample(test_data, min(len(test_data), 10))
    context.bot_data["test_data_iter"] = iter(test_data)
    context.user_data["result"] = {"result": 0, "max_result": len(test_data)}
    context.bot.send_message(chat_id=update.effective_chat.id, text='Начем опрос.')
    next_question(update, context)
    return 1


def next_question(update: Update, context: CallbackContext):
    try:
        next_test_data = next(context.bot_data["test_data_iter"])
    except StopIteration:
        return stop(update, context)
    question = next_test_data["question"]
    context.bot_data["right_answer"] = next_test_data["response"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=question)
    return 1


def handle_answer(update: Update, context: CallbackContext):
    right_answer = context.bot_data["right_answer"]
    if update.message.text.lower() == right_answer.lower():
        context.user_data["result"]["result"] += 1
    return next_question(update, context)


def stop(update, context):
    result = context.user_data["result"]
    result = f"{result['result']}/{result['max_result']}"
    text = f"Ваш результат: {result}"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Опрос окончен")
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Начать заново? (/start)")
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, handle_answer)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
