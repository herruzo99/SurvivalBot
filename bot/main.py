from telegram.ext import Updater
from environs import Env
import logging

from telegram.utils.request import Request

import bot.handlers as handlers

import telegram.bot
from telegram.ext import messagequeue as mq
from telegram.ext.dictpersistence import DictPersistence


class MQBot(telegram.bot.Bot):
    """Implementación actual del retardo de la cola para evitar superar el límite de envio de mensajes por segundo
    https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits"""

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


def data_store(context):
    persistent = context.job.context
    user_data = persistent.user_data_json
    f = open("data/user_data.json", "w+")
    f.write(user_data)
    f.close()


def create_persistent():
    try:
        f = open("data/user_data.json", "r")
        user_content = f.read()
    except FileNotFoundError:
        user_content = ""
    return DictPersistence(user_data_json=user_content)


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    """Implementacio4ón actual del retardo de envio"""
    queue = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017)
    # set connection pool size for bot
    request = Request(con_pool_size=8)
    bot = MQBot(env("TOKEN"), request=request, mqueue=queue)
    """Hasta quí la implementación actual del límite de envio"""

    persistent = create_persistent()

    updater = Updater(bot=bot, persistence=persistent, use_context=True)
    dispatcher = updater.dispatcher
    handlers.handlers(dispatcher)
    updater.start_polling()

    jq = updater.job_queue
    jq.run_repeating(data_store, interval=10, context=persistent)


if __name__ == "__main__":
    main()
