import telegram
from telegram.ext import Updater, Filters, MessageHandler, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import telegram_bot.map_api as map_api
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
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
# user_info = {}


def start(update, context):
    update.message.reply_text(
        "Я чат-бот 🤖, который поможет тебе определить твою проблему и предложить услугу МФЦ. При желании, после того"\
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
    context.user_data['first_name'] = update.message.text
    update.message.reply_text(f'Хорошо, {context.user_data["first_name"]}, теперь введите свою фамилию')
    return 3


def set_second_name(update, context):
    context.user_data['second_name'] = update.message.text
    update.message.reply_text('Для регистрации необходимы Ваши паспортные данные ... ')
    return 5


def set_passport(update, context):
    pass


def gender(update, context):
    context.user_data['passport'] = update.message.text
    msg = update.message
    msg.delete()
    update.message.reply_text(f'Паспортные данные введены... {context.user_data["passport"]}')
    # Инвайт кнопка
    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='👧', callback_data='👧'),
         telegram.InlineKeyboardButton(text='👨', callback_data='👨')]
    ])
    update.message.reply_text('Выбери свой пол ',
                              reply_markup=keyboard)
    return 5


def set_girl(update, context):
    context.user_data['gender'] = 'муж'
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
    context.user_data['gender'] = 'муж'
    query = update.callback_query
    query.answer('👨')

    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='Сохранить', callback_data='Сохранить'),
         telegram.InlineKeyboardButton(text='Отмена', callback_data='Отмена')]
    ])
    query.edit_message_text(f'Сохранить изменения? {context.user_data["gender"]}',
                            reply_markup=keyboard)
    return 7


def save_changes(update, context):
    # add user in db
    query = update.callback_query
    query.edit_message_text(text=f'Регистрация завершена {[[k, v] for k, v in context.user_data.items()]}')
    return ConversationHandler.END


# Реализовать конечный автомат с передачей данных между состяниями
registration_handler = ConversationHandler(
    # Регистрация человка (можно добавить и удаление)
    entry_points=[CommandHandler('registration', registration)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, registration, pass_user_data=True),
            CallbackQueryHandler(agreement, pattern='Да', pass_user_data=True),
            CallbackQueryHandler(disagreement, pattern='Нет', pass_user_data=True)
            ],
        2: [MessageHandler(Filters.text & ~Filters.command, set_first_name, pass_user_data=True),
            CallbackQueryHandler(agreement, pattern='Да', pass_user_data=True),
            CallbackQueryHandler(disagreement, pattern=' Нет', pass_user_data=True)
            ],
        3: [MessageHandler(Filters.text & ~Filters.command, set_second_name, pass_user_data=True)],
        4: [MessageHandler(Filters.text & ~Filters.command, set_passport, pass_user_data=True)],
        5: [MessageHandler(Filters.text & ~Filters.command, gender, pass_user_data=True),
            CallbackQueryHandler(set_girl, pattern='^' + '👧' + '$', pass_user_data=True),
            CallbackQueryHandler(set_man, pattern='^' + '👨' + '$', pass_user_data=True)],
        7: [CallbackQueryHandler(disagreement, pattern='Отмена', pass_user_data=True),
            CallbackQueryHandler(save_changes, pattern='Сохранить', pass_user_data=True)],

    },
    fallbacks=[CommandHandler('end', stop)]
)


def admission(update, context):
    # Вывести список Городов Амурской области
    keyboard = telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text='Благовещенск 🌆', callback_data='Благовещенск'),
         telegram.InlineKeyboardButton(text='Шимановск 🌇', callback_data='Шимановск')],
        [telegram.InlineKeyboardButton(text='Свободный 🏙️', callback_data='Свободный'),
         telegram.InlineKeyboardButton(text='Белогорск 🌌', callback_data='Белогорск')]
    ])
    update.message.reply_text('Выбери город Амурской области, где хочешь записаться ',
                              reply_markup=keyboard)
    return 1


def define_city(update, context):
    query = update.callback_query
    query.edit_message_text(f'Вы выбрали {query.data}\nТеперь пишите Вашу проблему')
    return 2


def define_service(update, context):
    # Установить услугу и узнать, по какому адресу предоставить услугу
    update.message.reply_text('Теперь выбери МФЦ')
    db_sess = create_session()

    keyboard = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(
        text=mfc.address,
        callback_data=mfc.address
    )] for mfc in db_sess.query(MFC).all()])
    update.message.reply_text('Выбери адрес, где тебе удобнее всего ',
                              reply_markup=keyboard)
    return 2


def set_mfc(update, context):
    query = update.callback_query
    query.edit_message_text('МФЦ выбрана ' + ' ✅.\nВыбрать дату приема?')
    return 3


def calendar_init(update, context):
    calendar, step = DetailedTelegramCalendar().build()
    if update.message.text.lower() == 'да':
        context.bot.send_photo(
            update.message.chat_id,
            map_api.get_static_api(),
            caption='Геолокация МФЦ'
        )
        update.message.reply_text(f"Выберите время приема {LSTEP[step]}", reply_markup=calendar)
    return 3


def set_admission_date(update, context):
    # send map
    return ConversationHandler.END


def set_calendar_date(update, context):
    query = update.callback_query
    result, key, step = DetailedTelegramCalendar().process(query.data)
    if not result and key:
        query.edit_message_text(f"Выбрано {LSTEP[step]}", reply_markup=key)
    elif result:
        # ! -------------------------
        keyboard = telegram.InlineKeyboardMarkup([
            [telegram.InlineKeyboardButton(text='9:30', callback_data='9:30'),
             telegram.InlineKeyboardButton(text='10:30', callback_data='10:30'),
             telegram.InlineKeyboardButton(text='11:30', callback_data='11:30')],
            [telegram.InlineKeyboardButton(text='13:30', callback_data='13:30'),
             telegram.InlineKeyboardButton(text='14:30', callback_data='14:30'),
             telegram.InlineKeyboardButton(text='15:30', callback_data='15:30')]
        ])
        query.edit_message_text(f"Вы выбрали дату {result}. Выберите время:", reply_markup=keyboard)
        return 4
    return 3


def set_time(update, context):
    query = update.callback_query
    query.edit_message_text(query.data)
    # Подтверждение записи на услугу
    return 5


admission_handler = ConversationHandler(
    entry_points=[CommandHandler('admission', admission)],
    states={
        1: [
            # MessageHandler(Filters.text & ~Filters.command, define_city, pass_user_data=True),
            CallbackQueryHandler(define_city, pass_user_data=True)],
        2: [MessageHandler(Filters.text & ~Filters.command, define_service, pass_user_data=True),
            CallbackQueryHandler(set_mfc, pass_user_data=True)],
        3: [MessageHandler(Filters.text & ~Filters.command, calendar_init, pass_user_data=True),
            CallbackQueryHandler(set_calendar_date, pattern=DetailedTelegramCalendar.func, pass_user_data=True)],
        4: [CallbackQueryHandler(set_time, pattern=r'\d\d.\d\d', pass_user_data=True)],
        5: [
            MessageHandler(Filters.text & ~Filters.command, set_admission_date, pass_user_data=True)
        ]
    },
    fallbacks=[CommandHandler('end', stop)]
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
    reply_keyboard = [['/admission', '/registration']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

    main()
