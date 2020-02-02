from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Dispatcher
from telegram.ext.dispatcher import run_async
from core.gameEngine import GameEngine
import logging

from core.player import Player


def handlers(dispatcher: Dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    game_handler = CommandHandler('game', game)
    dispatcher.add_handler(game_handler)

    turn_handler = CommandHandler('turn', turn)
    dispatcher.add_handler(turn_handler)

    dispatcher.add_error_handler(error_callback)


@run_async
def start(update: Update, context: CallbackContext):  # for start url base64.urlsafe_b64encode
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido al bot de survival")


game_alive = {}


@run_async
def game(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if group_id in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida ya empezada")

    else:
        if len(context.args) > 0:
            players = []
            for person in context.args:
                players.append(Player(person))
        else:
            players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        game_alive[group_id] = GameEngine(players)
        context.bot.send_message(chat_id=group_id, text="Empieza la partida")
        turn(update, context)


@run_async
def turn(update: Update, context: CallbackContext):
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


def error_callback(update, context):
    logger = logging.getLogger()
    logger.warning('Update "%s" caused error "%s"', update, context.error)
