import json
import logging
import os
from enum import Enum


def load_dictionary(root_dir, dict_type):
    with open(os.path.join(root_dir, dict_type.value), encoding='utf-8') as json_file:
        dictionary = json.load(json_file)
        logging.info("File {} loaded with content: \n {}".format(json_file.name,
                                                                 json.dumps(dictionary, ensure_ascii=False, indent=4,
                                                                            sort_keys=True)))
        return dictionary


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
