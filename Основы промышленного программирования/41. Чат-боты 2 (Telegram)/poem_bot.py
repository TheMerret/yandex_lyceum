import logging
import os

from telegram import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

POEM = """Зима!.. Крестьянин, торжествуя,
На дровнях обновляет путь;
Его лошадка, снег почуя,
Плетется рысью как-нибудь;
Бразды пушистые взрывая,
Летит кибитка удалая;
Ямщик сидит на облучке
В тулупе, в красном кушаке.
Вот бегает дворовый мальчик,
В салазки жучку посадив,
Себя в коня преобразив;
Шалун уж заморозил пальчик:
Ему и больно и смешно,
А мать грозит ему в окно..."""


class Poem:

    def __init__(self, text: str):
        self.rows = text.splitlines()
        self.iter_rows = iter(self.rows)
        self.cur_row = None

    def __next__(self):
        nxt_row = next(self.iter_rows)
        self.cur_row = nxt_row
        return nxt_row


poem = Poem.__new__(Poem)


def start(update: Update, context: CallbackContext):
    poem.__init__(POEM)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Продолжайте за мной!')
    next_row(update, context)
    return 1


def next_row(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=next(poem))


def guess_row(update: Update, context: CallbackContext):
    current_row = poem.cur_row if context.user_data.get('suphler_activated', False) else next(poem)
    if update.message.text == current_row:
        context.user_data["suphler_activated"] = False
        try:
            next_row(update, context)
        except StopIteration:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Вы молодец. Мы закончили! (/start чтобы начать заново)")
            return ConversationHandler.END
        return 1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Неверно, попробуйте еще раз (подсказка - /suphler)")
        return 2


def suphler(update: Update, context: CallbackContext):
    context.user_data["suphler_activated"] = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="Повторите:")
    context.bot.send_message(chat_id=update.effective_chat.id, text=poem.cur_row)
    return 1


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, guess_row)],
            2: [CommandHandler('suphler', suphler)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
