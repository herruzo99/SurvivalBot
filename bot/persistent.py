import os

from telegram.ext import DictPersistence


def data_store(context):  # Usando JSON
    persistent = context.job.context
    user_data = persistent.user_data_json

    path = "data"
    if not os.path.exists(path):
        os.makedirs(path)

    filename = "user_data.json"
    with open(os.path.join(path, filename), 'w+') as temp_file:
        temp_file.write(user_data)



def create_persistent():
    try:
        path = "data"
        filename = "user_data.json"
        f = open(os.path.join(path, filename), 'w+')
        user_content = f.read()
    except FileNotFoundError:
        user_content = ""
    return DictPersistence(user_data_json=user_content)
