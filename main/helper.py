import json
import logging
import os
from enum import Enum
from pathlib import Path


def create_sample_file():
    data = {"Сообщение1": "Ответ1",
            "Сообщение2": "Ответ2",
            "Сообщение3": "Ответ3",
            "Сообщение4": "Ответ5",
            "Сделай меня админом": "А ху ху не хо хо?"}

    def write_to_file(data_to_write):
        path = Path(__file__).parent / "data" / "sample_file.json"

        with open(path, "w") as write_file:
            j = json.dumps(data_to_write, ensure_ascii=False, indent=4, sort_keys=True)
            write_file.write(j)
            print(j)

    write_to_file(data)


def load_dictionary(root_dir, dict_type):

    with open(os.path.join(root_dir, dict_type.value)) as json_file:
        dict = json.load(json_file)
        logging.debug("File {} loaded with content: \n {}".format(json_file.name, json.dumps(dict, ensure_ascii=False, indent=4, sort_keys=True)))
        return dict

class ChatDict(Enum):
    User = os.path.join("data", "conversation_dictionary.json")
    Admin = os.path.join("data", "admin_conversation_dictionary.json")


def log(message, message_type, response_to=None):
    if message_type == MessageType.REQUEST:
        logging.info("MSG (id ={}):Пользователь {} (id={}) отправил сообщение c текстом:\n{}".format(
            message.message_id,
            str(message.from_user.first_name) + " " + str(message.from_user.last_name),
            str(message.from_user.id),
            message.text
        ))
    if message_type == MessageType.RESPONSE:
        logging.info(
            "MSG (id ={}): В ответ на сообщение {} пользователя {} (id={}) бот отправил текст: \n {}".format(
                message.message_id,
                response_to,
                str(message.chat.first_name) + " " + str(message.chat.last_name),
                str(message.chat.id),
                message.text
            ))

class MessageType(Enum):
    REQUEST = 1
    RESPONSE = 2