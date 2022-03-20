from telegram.ext import Updater, Filters, MessageHandler, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import telegram_bot.map_api as map_api
import pandas as pd
from database.entity import *
from database.db_session import *
import csv
import faq_write
from FAQ.model import Faq
import numpy as np
import deeppavlov
from deeppavlov import configs
from deeppavlov.core.common.file import read_json
from deeppavlov.core.commands.infer import build_model
from deeppavlov import configs, train_model
import logging
from passporteye import read_mrz  # Машиночитаемая зона паспорта для регистрации в базе данных (благодарность на гитхабе)

logging.basicConfig(level=logging.ERROR)
global_init("postgre1")
with open('../../token_teleg') as token_file:
    TOKEN = token_file.read().strip()


def start(update, context):
    update.message.reply_text(
        "I am echo-bot",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text("I am can't help you")


def echo(update, context):
    update.message.reply_text(update.message.text)


def faq(update, context):
    question = ' '.join(context.args)
    faq = Faq(faq_write.faq_write())
    # faq = Faq('../FAQ/data_faq_mfc.csv')
    faq.train()
    answer = faq.infer(question)[0][0]
    update.message.reply_text(answer)


def news(update, context):
    context.bot.send_photo(
        update.message.chat_id,
        map_api.get_static_api(),
        caption='Вот тебе карта'
    )


def close(update, context):
    update.message.reply_text('ok', reply_markup=ReplyKeyboardRemove())


def remove_job(name, context):
    current_job = context.job_queue.get_jobs_by_name(name)
    if not current_job:
        return False
    for job in current_job:
        job.schedule_removal()
    return True


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся')


def set_timer(update, context):
    chat_id = update.message.chat_id

    try:
        due = int(context.args[0])  # секунды таймера
        if due < 0:
            return 0
        job_removed = remove_job(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
        text = f"Вернусь через {due} секунд"
        if job_removed:
            text += ' Старая задача удалена'
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <сек>')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера'
    update.message.reply_text(text)


def stop():
    # Conversion END
    return ConversationHandler.END


def registration(update, context):
    update.message.reply_text("registration")
    return 1


def set_first_name(update, context):
    update.message.reply_text('first' + update.message.text)
    return 2


def set_second_name(update, context):
    update.message.reply_text('second' + update.message.text)
    return 3


def set_passport():
    return 4


def set_gender():
    return 5


def add_user():
    # add user in db
    return ConversationHandler.END


# Реализовать конечный автомат
registration_handler = ConversationHandler(
    # Регистрация человка (можно добавить и удаление)
    entry_points=[CommandHandler('registration', registration)],
    states={
        1: [MessageHandler(Filters.text, set_first_name)],
        2: [MessageHandler(Filters.text, set_second_name)],
        3: [MessageHandler(Filters.text, set_passport)],
        4: [MessageHandler(Filters.text, set_gender)],
        5: [MessageHandler(Filters.text, add_user)],

    },
    fallbacks=[CommandHandler('stop', stop)]
)


def admission(update, context):
    return 1


def define_city(update, context):
    return 2


def define_service(update, context):
    update.message.reply_text('second' + update.message.text)
    return 3


def define_mfc():
    return 4


def set_admission_date():
    # send map
    return ConversationHandler.END


admission_handler = ConversationHandler(
    entry_points=[CommandHandler('admission', admission)],
    states={
        1: [MessageHandler(Filters.text, define_city)],
        2: [MessageHandler(Filters.text, define_service)],
        3: [MessageHandler(Filters.text, define_mfc)],
        4: [MessageHandler(Filters.text, set_admission_date)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("faq", faq, pass_args=True))
    dp.add_handler(CommandHandler("news", news))
    # dp.add_handler(CommandHandler("registration", registration)) Нужно убрать для работы ConvertionalHandler
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer, pass_chat_data=True))
    # dp.add_handler(MessageHandler(Filters.text, echo))  # регистрация обработчика в диспетчере
    dp.add_handler(registration_handler)
    dp.add_handler(admission_handler)

    updater.start_polling()  # запуск цикла приема и обработки сообщений

    updater.idle()


if __name__ == "__main__":
    reply_keyboard = [['/faq', '/news'], ['/registration']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

    main()
