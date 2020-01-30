from telegram.ext import Updater
from environs import Env
import logging
import bot.handlers as handlers


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(token=env("TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    handlers.handlers(dispatcher)

    updater.start_polling()


if __name__ == "__main__":
    main()
