from typing import Any
import telebot

from src.settings.config import TELEGRAM_TOKEN
from src.settings.config import LOGIN
from src.settings.config import PASSWORD
from src.parser.manager import Parser
from src.parser.models import UserInformation


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
    parser = Parser(login=LOGIN, password=PASSWORD)
    result: UserInformation = parser.user_info()
    msg = f"""Общая информация о лицевом счёте:
    Абонент: {result.subscriber}
    Адрес помещения: {result.address}
    Площадь (Общая/жилая): {result.living_space}
    Форма собственности: {result.form_of_ownership}
    Телефон: {result.phone}
    Электронная почта: {result.email}
    Зарегистрировано: {result.registered_people}
    Временно отсутствует: {result.unavailable_people}
    Задолженность: {result.indebtedness}
    """
    app.reply_to(message, msg)


@app.message_handler(commands=['logout'])
def send_logout(message: Any):
    app.reply_to(message, "Howdy, how are you doing?")


@app.message_handler(func=lambda message: True)
def echo_all(message: Any):
    app.reply_to(message, message.text)


if __name__ == "__main__":
    app.infinity_polling()
