import os
import logging

from telegram import Update
from telegram.ext import (Updater, MessageHandler, Filters, CallbackContext, CommandHandler,
                          ConversationHandler, CallbackQueryHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


TOKEN = os.getenv("TOKEN")


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
    "Привет. Пройдите небольшой опрос, пожалуйста!\n"
    "Вы можете прервать опрос, послав команду /stop.\n"
    "В каком городе вы живёте? (/skip пропустить этот вопос)")
    logger.info("dialog started")
    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


def skip_first_question(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Тогда другой вопрос.')
    anon_first_response(update, context)
    return 2


def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {locality}?")
    logger.info("second question")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    logger.info(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


def anon_first_response(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Какая погода у вас за окном?")
    logger.info("second question")
    return 2


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response),
                CommandHandler('skip', skip_first_question)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
