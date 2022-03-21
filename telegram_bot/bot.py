import telegram
from telegram.ext import Updater, Filters, MessageHandler, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
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
from passporteye import \
    read_mrz  # Машиночитаемая зона паспорта для регистрации в базе данных (благодарность на гитхабе)

logging.basicConfig(level=logging.ERROR)
global_init("postgre1")
with open('../../token_teleg') as token_file:
    TOKEN = token_file.read().strip()


def start(update, context):
    update.message.reply_text(
        "Я чат-бот 🤖, который поможет тебе определить твою проблему и предложить услугу МФЦ. При желании, после того" \
        " как ты зарегистрируешься, можешь записаться на прием, я тебе поставлю напоминалку 😉 ✅",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text("Я чат-бот 🤖, который поможет тебе определить твою проблему и предложить услугу МФЦ."
                              " При желании, после того"
                              " как ты зарегистрируешься, можешь записаться на прием, я тебе поставлю напоминалку 😉 ✅")


def echo(update, context):
    update.message.reply_text(update.message.text)


def faq(update, context):
    question = ' '.join(context.args)
    faq = Faq(faq_write.faq_write())
    # faq = Faq('../FAQ/data_faq_mfc.csv')
    faq.train()
    answer = faq.infer(question)[0][0]
    update.message.reply_text(answer)


def define_service(update, context):
    # Функция определния сервиса, необходимого для определния услуги
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

# Установка напоминания
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


#  Работа с обработчиками
def stop(update, context):
    # Conversion END
    return ConversationHandler.END


def registration(update, context):
    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='Да', callback_data='Да'),
         telegram.InlineKeyboardButton(text='Нет', callback_data='Нет')]
    ])
    update.message.reply_text('Начать процесс регистрации?',
                              reply_markup=keyboard)
    return 1


def agreement(update, context):
    query = update.callback_query
    query.answer('Введите свое имя')
    query.edit_message_text(text='Введите свое имя')
    return 2


def disagreement(update, context):
    query = update.callback_query
    query.edit_message_text(text='Регистрация отменена')
    return ConversationHandler.END


def set_first_name(update, context):
    update.message.reply_text(f'Хорошо, {update.message.text}, теперь введите свою фамилию')
    return 3


def set_second_name(update, context):
    update.message.reply_text('Для регистрации необходимы Ваши паспортные данные ... ')
    return 5


def set_passport(update, context):
    pass


def gender(update, context):
    # Инвайт кнопка
    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='👧', callback_data='👧'),
         telegram.InlineKeyboardButton(text='👨', callback_data='👨')]
    ])
    update.message.reply_text('Выбери свой пол ',
                              reply_markup=keyboard)
    return 5


def set_girl(update, context):
    query = update.callback_query
    query.answer('👧')

    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='Сохранить', callback_data='Сохранить'),
         telegram.InlineKeyboardButton(text='Отмена', callback_data='Отмена')]
    ])
    query.edit_message_text('Сохранить изменения? ',
                            reply_markup=keyboard)
    return 7


def set_man(update, context):
    query = update.callback_query
    query.answer('👨')

    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='Сохранить', callback_data='Сохранить'),
         telegram.InlineKeyboardButton(text='Отмена', callback_data='Отмена')]
    ])
    query.edit_message_text('Сохранить изменения? ',
                            reply_markup=keyboard)
    return 7


def save_changes(update, context):
    # add user in db
    query = update.callback_query
    query.edit_message_text(text='Регистрация завершена')
    return ConversationHandler.END


# Реализовать конечный автомат с передачей данных между состяниями
registration_handler = ConversationHandler(
    # Регистрация человка (можно добавить и удаление)
    entry_points=[CommandHandler('registration', registration)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, registration),
            CallbackQueryHandler(agreement, pattern='Да'),
            CallbackQueryHandler(disagreement, pattern='Нет')
            ],
        2: [MessageHandler(Filters.text & ~Filters.command, set_first_name),
            CallbackQueryHandler(agreement, pattern='Да'),
            CallbackQueryHandler(disagreement, pattern=' Нет')
            ],
        3: [MessageHandler(Filters.text & ~Filters.command, set_second_name)],
        4: [MessageHandler(Filters.text & ~Filters.command, set_passport)],
        5: [MessageHandler(Filters.text & ~Filters.command, gender),
            CallbackQueryHandler(set_girl, pattern='^' + '👧' + '$'),
            CallbackQueryHandler(set_man, pattern='^' + '👨' + '$')],
        7: [CallbackQueryHandler(disagreement, pattern='Отмена'),
            CallbackQueryHandler(save_changes, pattern='Сохранить')],

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
        1: [MessageHandler(Filters.text & ~Filters.command, define_city)],
        2: [MessageHandler(Filters.text & ~Filters.command, define_service)],
        3: [MessageHandler(Filters.text & ~Filters.command, define_mfc)],
        4: [MessageHandler(Filters.text & ~Filters.command, set_admission_date)]
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
