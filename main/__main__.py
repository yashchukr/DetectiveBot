import configparser

import telebot
from telebot import TeleBot

# from main.helper import *
# from main.loggerinitializer import *

# Загружаєм токен бота в телеграме из файла кофигурации config.ini
config = configparser.ConfigParser()
config.read("CONFIG.INI")
token = config.get("telegram", "token")