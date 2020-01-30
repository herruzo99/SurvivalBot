from telegram.ext import CommandHandler


def handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido a SurvivalBot")
