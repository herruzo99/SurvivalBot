import os

from telegram.ext import PicklePersistence, CallbackContext


def store(context: CallbackContext):
    context.job.context.flush()


def get_storage():
    return PicklePersistence(os.path.join("data", "user_data.pickle"), on_flush=True)
