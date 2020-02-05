import time

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, Dispatcher, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from core.gameEngine import GameEngine
import logging

from core.player import Player


def handlers(dispatcher: Dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    game_handler = CommandHandler('game', game)
    dispatcher.add_handler(game_handler)
    start_game_handler = CommandHandler('start_game', start_game)
    dispatcher.add_handler(start_game_handler)

    add_extra_handler = CommandHandler('add_extra', add_extra)
    dispatcher.add_handler(add_extra_handler)

    create_player_handler = CommandHandler('create_player', create_player)
    dispatcher.add_handler(create_player_handler)
    show_player_handler = CommandHandler('show_player', show_player)
    dispatcher.add_handler(show_player_handler)

    turn_callback = CallbackQueryHandler(turn, pattern="next")
    dispatcher.add_handler(turn_callback)

    dispatcher.add_error_handler(error_callback)


game_alive = {}


@run_async
def start(update: Update, context: CallbackContext):  # for start url base64.urlsafe_b64encode
    if context.args:
        game_id = int(context.args[0])
        if game_id in game_alive:
            if "player" not in context.user_data:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="No tienes un jugador creado, puedes crarlo con /create_player")
            else:
                game_alive[game_id].add_player(context.user_data["player"])
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Te has unido correctamente a la partida")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Vaya, esa partida no existe")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido al bot de survival")


@run_async
def game(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if group_id in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida ya empezada")

    else:
        g = GameEngine()
        game_alive[group_id] = g
        butom = InlineKeyboardMarkup(
            [[InlineKeyboardButton("join", url="https://t.me/survivial_bot?start=" + str(group_id))]])
        context.bot.send_message(chat_id=group_id,
                                 text="Empezando partida, a unirse!\n Para empezar la partida usar /start_game\n "
                                      "También se pueden añadir jugadores extra con /add_extra <nombre>, <nombre>*",
                                 reply_markup=butom)


@run_async
def start_game(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if group_id not in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida no existe")
    g = game_alive[group_id]
    if len(g.players) > 4:
        context.bot.send_message(chat_id=group_id, text="Empieza!!!")
        turn(update, context)
    else:
        context.bot.send_message(chat_id=group_id, text="No hay suficientes jugadores")


def add_extra(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if not context.args:
        context.bot.send_message(chat_id=group_id,
                                 text="Hay que dar un nombre \"/add_extra <nombre> (se pueden poner varios separando "
                                      "por comas\"")
    elif group_id not in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida no existe")
    else:
        names = ' '.join(map(str, context.args))
        names = names.split(",")
        g = game_alive[group_id]
        for name in names:
            name = name.strip()
            if name is not "":
                g.add_player(Player(name))


@run_async
def turn(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if group_id not in game_alive:
        context.bot.send_message(chat_id=group_id, text="Partida no empezada")

    else:
        game_group = game_alive[group_id]
        playing = game_group.turn()
        text = ""
        for t in game_group.get_log():
            text += "\n" + t

        if update.callback_query:
            message = update.callback_query.message
            chat_id = message.chat.id
            message_id = message.message_id
            context.bot.editMessageReplyMarkup(chat_id, message_id)

        if playing:
            butom = InlineKeyboardMarkup([[InlineKeyboardButton("next", callback_data="next")]])
        else:
            butom = ""

        context.bot.send_message(chat_id=group_id, text=text, reply_markup=butom)

        if not playing:
            context.bot.send_message(chat_id=group_id, text=game_group.get_end())
            context.bot.send_message(chat_id=update.effective_chat.id, text="Fin de la partida")
            del game_alive[group_id]


def show_player(update: Update, context: CallbackContext):
    group_id = update.effective_chat.id
    if update.effective_chat.type != "private":
        context.bot.send_message(chat_id=group_id, text="Solo se puede usar en chat privado")

    if "player" not in context.user_data:
        context.bot.send_message(chat_id=group_id, text="No tienes un jugador creado")
    else:
        pass
        context.bot.send_message(chat_id=group_id, text="Jugador: " + context.user_data["player"].name)


def create_player(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if update.effective_chat.type != "private":
        context.bot.send_message(chat_id=chat_id, text="Solo se puede usar en chat privado")

    if "player" in context.user_data:
        context.bot.send_message(chat_id=chat_id, text="Ya tienes un jugador creado")
    else:
        context.user_data["player"] = Player("juan")
        context.bot.send_message(chat_id=chat_id, text="Jugador creado")


def error_callback(update: Update, context: CallbackContext):
    logger = logging.getLogger()
    logger.warning('Update "%s" caused error "%s"', update, context.error)
