import os
import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler

TOKEN = os.getenv("TOKEN")

start_keyboard = [["/dice", "/timer"]]
dice_keyboard = [["/dice_roll 6", "/dice_roll 6 2", "/dice_roll 20"],
                 ["/back"]]
timer_keyboard = [["/set_timer 30", "/set_timer 60", "/set_timer 300"],
                  ["/back"]]
close_timer_keyboard = [["/close"]]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
close_timer_markup = ReplyKeyboardMarkup(close_timer_keyboard, one_time_keyboard=False)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Привет! выберите функцию""",
                             reply_markup=start_markup)


def dice(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Выберите кость.",
                             reply_markup=dice_markup)


def dice_roll(update: Update, context: CallbackContext):
    args = context.args
    try:
        args = list(map(int, args))
    except (TypeError, ValueError):
        text = "Введите число"
    else:
        if len(args) == 2:
            num = args[0]
            results = [random.SystemRandom().randint(1, num) for i in range(args[1])]
            text = " ".join(map(str, results))
        elif len(args) == 1:
            num = args[0]
            res = random.SystemRandom().randint(1, num)
            text = str(res)
        else:
            text = "Введите одно или два числа"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=dice_markup)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f"Засек {due} секунд!"
        context.bot_data.update({"timer": due})
        if job_removed:
            text += ' Старая задача удалена.'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text,
                                 reply_markup=close_timer_markup)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


def task(context):
    """Выводит сообщение"""
    job = context.job
    time_duration = context.bot_data["timer"]
    text = f"{time_duration} сек истекло"
    context.bot.send_message(job.context, text=text, reply_markup=timer_markup)


def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=timer_markup)


def timer(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Выберите таймер",
                             reply_markup=timer_markup)


def back(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Выберите функцию",
                             reply_markup=start_markup)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("dice_roll", dice_roll))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("set_timer", set_timer))
    dp.add_handler(CommandHandler("close", unset))
    dp.add_handler(CommandHandler("back", back))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
