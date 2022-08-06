from typing import Any
import telebot
from dotenv import set_key

from src.parser.manager import manager
from src.settings.config import TELEGRAM_TOKEN


app = telebot.TeleBot(token=TELEGRAM_TOKEN,
                      parse_mode=None)


@app.message_handler(commands=['start'])
def send_start(message: Any):
    app.reply_to(message, "Howdy, how are you doing?")


@app.message_handler(commands=['help'])
def send_help(message: Any):
    app.reply_to(message, "Howdy, how are you doing?")


@app.message_handler(commands=['login'])
def send_login(message: Any):
    app.reply_to(message, "Howdy, how are you doing?")


@app.message_handler(commands=['logout'])
def send_logout(message: Any):
    app.reply_to(message, "Howdy, how are you doing?")


@app.message_handler(func=lambda message: True)
def echo_all(message: Any):
    app.reply_to(message, message.text)


if __name__ == "__main__":
    app.infinity_polling()
    result = manager()
    if not result:
        print("NO COOKIES!")
        exit()

    if isinstance(result, str):
        set_key(".env", key_to_set="SESSIONID", value_to_set=result)
        exit()
