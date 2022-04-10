import logging
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater, MessageHandler, Filters, CallbackContext, CommandHandler,
                          ConversationHandler, )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

HALL_KEYBOARDS = {
    0: [[1], ["/exit"]],
    1: [[2], ['/exit']],
    2: [[3]],
    3: [[1, 4]],
    4: [[1]]
}

HALL_DESCRIPTIONS = {
    1: "В данном зале представлены античные скульптуры",
    2: "В данном зале представлены русские художники серебряного века",
    3: "В данном зале представлены работы эпохи возрождения",
    4: "В данном зале представлены французские импрессионисты"
}

HALL_PREVIEWS = {
    1: "Античность",
    2: "Серебряный век",
    3: "Ренессанс",
    4: "Ипрессионизм",
}


def start(update: Update, context: CallbackContext):
    logger.info("dialog started")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Добро пожаловать! Выбиртайте действия с помощью кнопок."
                                  " Пожалуйста, сдайте верхнюю одежду в гардероб!")
    context.bot_data["hall_number"] = 0
    next_hall(update, context)
    return 1


def next_hall(update: Update, context: CallbackContext):
    hall_number = context.bot_data["hall_number"]
    next_hall_numbers = HALL_KEYBOARDS[hall_number][0]
    hall_previews = [f"{i}: {HALL_PREVIEWS[i]}" for i in next_hall_numbers]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Следующие залы:\n" + "\n".join(hall_previews)
                             )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Выберите: ",
                             reply_markup=ReplyKeyboardMarkup(
                                 HALL_KEYBOARDS[hall_number], one_time_keyboard=True
                             ))
    return 1


def hall(update: Update, context: CallbackContext):
    number = int(update.message.text)
    context.bot_data["hall_number"] = number
    update.message.reply_text(HALL_DESCRIPTIONS[number])
    next_hall(update, context)
    logger.info(f"hall number {number}")
    return 1


def ext(update, context):
    update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            0: [MessageHandler(Filters.text & ~Filters.command, next_hall)],
            1: [MessageHandler(Filters.text & ~Filters.command, hall)],
        },

        fallbacks=[CommandHandler('exit', ext)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
