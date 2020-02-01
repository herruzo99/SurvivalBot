from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from threading import Thread
from core.gameEngine import GameEngine


def handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('game', game)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('turn', turn)
    dispatcher.add_handler(start_handler)

@run_async
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido a SurvivalBot")


game_alive = {}

@run_async
def game(update, context):
    group_id = update.effective_chat.id
    if group_id in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida ya empezada")

    else:
        game_alive[group_id] = GameEngine([1, 2, 3, 4, 5])
        context.bot.send_message(chat_id=group_id, text="Empieza la partida")
        turn(update, context)

@run_async
def turn(update, context):
    group_id = update.effective_chat.id
    if group_id not in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida no empezada")

    else:
        game_group = game_alive[group_id]
        status = game_group.turn()
        text = ""
        for t in game_group.get_log():
            text += "\n" + t
        context.bot.send_message(chat_id=group_id, text=text)

        if not status:
            context.bot.send_message(chat_id=group_id, text=game_group.get_end())
            context.bot.send_message(chat_id=update.effective_chat.id, text="Fin de la partida")
            del game_alive[group_id]
