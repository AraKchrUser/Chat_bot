from telegram.ext import Updater, Filters, MessageHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
TOKEN = "5059606687:AAFepvWE7Tcw9lWBe1HtHj1hMbEF-vs3qRA"


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
    update.message.reply_text('FAQ')


def news(update, context):
    update.message.reply_text("news")


def register(update, context):
    update.message.reply_text("register")


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


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("faq", faq))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer, pass_chat_data=True))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)  # регистрация обработчика в диспетчере

    updater.start_polling()  # запуск цикла приема и обработки сообщений

    updater.idle()


if __name__ == "__main__":
    reply_keyboard = [['/faq', '/news'], ['/register']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    main()
