import configparser

import telebot
from telebot import TeleBot

from main.helper import *
from main.loggerinitializer import *

# Загружаєм токен бота в телеграме из файла кофигурации config.ini
config = configparser.ConfigParser()
config.read("CONFIG.INI")
token = config.get("telegram", "token")

# определяем каталог выполнения скрипта
root_path = Path(__file__).parent

# инициализируем логер,
initialize_logger(root_path)
logging.info("-------------- START -----------------")

# Словарь админов бота: через запятую перечисляем ИД админов в виде "[идентификатор]:[True/False]" При False бот
# изначально будет работать с указанным пользователем в обычном режиме, а при True бот будет с работать с указанным
# пользователем в режиме обработки адимистративных команд. Пользователь, который указан в справочнике, может в любой
# момент перейти в административный режим отправив сообщение "Аз есмь твой богъ" или перейти в обычный режим,
# отправив сообщение "Хочу быть как все!"
admin_mode = {533723825: False, 470214517: False}

# Загружаем словарь вопросов-ответов из ../data/conversation_dictionary.json и
# ../data/admin_conversation_dictionary.json/
user_chat = load_dictionary(root_path, ChatDict.User)
admin_chat = load_dictionary(root_path, ChatDict.Admin)

# Запускаем бот
bot: TeleBot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    log(message, MessageType.REQUEST)

    if admin_mode.get(message.from_user.id) is not None and message.text == "Аз есмь твой богъ!" and not admin_mode.get(
            message.from_user.id):
        admin_mode[message.from_user.id] = True
        send_response(message, admin_chat["MAKEADMIN"].format(message.from_user.first_name))
    elif (False if admin_mode.get(message.from_user.id) is None else admin_mode.get(message.from_user.id)):
        process_admin_message(message)
    else:
        process_user_message(message)


# метод для обработки сообщений в режиме администратора. Словарик admin_chat используется исключительно для
# сокращения количества текста в коде.
def process_admin_message(message):
    if message.text == "Астанавитесь!!!":
        send_response(message, admin_chat.get("SHUTDOWN"))
        logging.info("----------- SHUTDOWN ----------")
        logging.info("Бот был остановлен пользователем {}")
        bot.stop_polling()
    elif message.text == "Хочу быть как все!":
        admin_mode[message.from_user.id] = False
        send_response(message, admin_chat.get("MAKEMORTAL"))
    elif message.text == "Аз есмь твой богъ!":
        admin_mode[message.from_user.id] = True
        send_response(message, admin_chat.get("ALREADYADMIN"))

    else:
        send_response(message, admin_chat.get("UNKNOWN"))


# метод для обработки сообщений в режиме пользвателя.
def process_user_message(message):
    if message.text == "А шо вы умеете?":
        list = []
        for key in user_chat.keys():
            if key not in {"UNKNOWN", "Аз есмь твой богъ"}:
                list.append(key)
        response = "Список вопросов:\n" + "\n".join(list)
        send_response(message, response)
    else:
        simple_user_message(message)


# метод для обработки сообщений в режиме пользвателя. Словарик user_chat определяет один ответ на один вопрос
def simple_user_message(message):
    text = user_chat.get(message.text)
    text = user_chat["UNKNOWN"] if text is None else text
    send_response(message, text)


def send_response(response_to, text):
    response = bot.send_message(response_to.chat.id, text)
    log(response, MessageType.RESPONSE, response_to.message_id)


bot.polling(none_stop=True, interval=0)
