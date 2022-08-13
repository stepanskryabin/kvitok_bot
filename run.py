import datetime
from typing import Any

import telebot
from telebot.types import Message

from src.settings.config import TELEGRAM_TOKEN
from src.parser.manager import LoginError, Parser
from src.parser.models import UserInformation
from src.gui.menu import main_menu
from src.gui.menu import agree_menu
from src.gui.menu import delete_menu
from src.gui.menu import company_menu
from src.gui.menu import pay_menu
from src.gui.menu import epd_menu
from src.gui.menu import settings_menu
from src.gui.menu import ipu_menu
from src.gui.message import AGREE
from src.parser.scope import CompanyName


app = telebot.TeleBot(token=TELEGRAM_TOKEN,
                      parse_mode=None)


def is_lic_number(username: str) -> bool:
    if username == "":
        return False

    if username.isnumeric():
        num = int(username)
        if num == 0 or num < 10000 or num > 9999999:
            return False
        else:
            return True
    else:
        return False


@app.message_handler(commands=['start'])
def send_start(message: Message):
    msg = app.send_message(message.chat.id,
                           text=AGREE,
                           reply_markup=agree_menu)
    app.register_next_step_handler(msg, check_agree)


def check_agree(message: Message):
    if message.text == "Согласен":
        msg = app.send_message(message.chat.id,
                               text="Выберите компанию:",
                               reply_markup=company_menu)
        app.register_next_step_handler(msg, check_company)
    elif message.text == "Не согласен":
        app.send_message(message.chat.id,
                         text="Пока!",
                         reply_markup=delete_menu)
    else:
        msg = app.send_message(message.chat.id,
                               text="..и ещё разок!?",
                               reply_markup=delete_menu)
        app.register_next_step_handler(msg, send_start)


def check_company(message: Message):
    if message.text == "ТСО Зиновы":
        company = CompanyName.TCO_ZYNOVY
    elif message.text == "УК Чепецкая":
        company = CompanyName.UK_CHEPETSKAYA
    elif message.text == "УК Боёвская":
        company = CompanyName.UK_BOEVSKAYA
    elif message.text == "Выход":
        app.send_message(message.chat.id,
                         text="Пока!",
                         reply_markup=delete_menu)
        return
    msg = app.send_message(message.chat.id,
                           text="Введите номер лицевого счёта:")
    app.register_next_step_handler(msg,
                                   check_user,
                                   company=company)


def check_user(message: Message,
               company: CompanyName):
    if is_lic_number(message.text):
        username = message.text
        msg = app.send_message(message.chat.id,
                               text="Введите пароль:")
        app.register_next_step_handler(msg,
                                       check_password,
                                       username,
                                       company)
    else:
        msg = app.send_message(message.chat.id,
                               text="Ошибка. Попытайтесь ещё раз:")
        app.register_next_step_handler(msg, check_user)


def check_password(message: Message,
                   username: str,
                   company: CompanyName):
    password = message.text
    parser = Parser(username=username,
                    password=password,
                    company=company)

    try:
        parser.login()
    except LoginError:
        msg = app.reply_to(message,
                           "Неверный логин или пароль.")
        app.register_next_step_handler(msg, send_start)
    else:
        msg = app.send_message(message.chat.id,
                               text="Авторизация прошла успешно!",
                               reply_markup=main_menu)
        app.register_next_step_handler(msg,
                                       check_menu_btn,
                                       parser=parser)


def return_to_main_menu(message: Message,
                        parser: Parser) -> None:
    app.register_next_step_handler(message,
                                   check_menu_btn,
                                   parser=parser)


def check_menu_btn(message: Message,
                   parser: Parser) -> Any:
    chat_id = message.chat.id
    user_unix_time = message.date
    match message.text:
        case 'Информация':
            result: UserInformation = parser.user_info()
            info = f"""Общая информация о лицевом счёте:\n
            Абонент: {result.subscriber}
            Адрес помещения: {result.address}
            Площадь (Общая/жилая): {result.living_space}
            Форма собственности: {result.form_of_ownership}
            Телефон: {result.phone}
            Электронная почта: {result.email}
            Зарегистрировано: {result.registered_people}
            Временно отсутствует: {result.unavailable_people}
            Задолженность: {result.indebtedness}
            Дополнительная информация: {result.indebtedness_info}
            Пени: {result.fine}
            """
            app.send_message(chat_id=chat_id, text=info)
            return_to_main_menu(message, parser)
        case 'Платежи':
            msg = app.send_message(chat_id=chat_id,
                                   text="Меню платежей.",
                                   reply_markup=pay_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Счётчики':
            msg = app.send_message(chat_id=chat_id,
                                   text="Меню счётчиков.",
                                   reply_markup=ipu_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Квитанции':
            msg = app.send_message(chat_id=chat_id,
                                   text="Меню квитанций.",
                                   reply_markup=epd_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Настройки':
            msg = app.send_message(chat_id=chat_id,
                                   text="Меню настроек.",
                                   reply_markup=settings_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Текущая история':
            pay_history = parser.pays_history(date_start="",
                                              date_stop="")
            for pay in pay_history:
                msg = f"{pay.data_income} - {pay.amount} - {pay.pay_agent}"
                app.send_message(chat_id=chat_id, text=msg)
            return_to_main_menu(message, parser)
        case 'Ввести период':
            pay_history = parser.pays_history(date_start="01.01.2022",
                                              date_stop="01.08.2022")
            for pay in pay_history:
                msg = f"{pay.data_income} - {pay.amount} - {pay.pay_agent}"
                app.send_message(chat_id=chat_id, text=msg)
            return_to_main_menu(message, parser)
        case 'Текущая квитанция':
            _datetime = datetime.date.fromtimestamp(user_unix_time)
            year = str(_datetime.year)
            month = str(_datetime.month)
            if len(month) == 1:
                month = month.zfill(2)
            current_period = "".join((year, month))
            epd = parser.print_epd(period=current_period)
            if epd is None:
                app.send_message(chat_id=chat_id, text="Файл отсутствует")
            else:
                app.send_document(chat_id=chat_id, document=open(epd, 'rb'))
            return_to_main_menu(message, parser)
        case 'Ввести период':
            _datetime = datetime.date.fromtimestamp(user_unix_time)
            year = str(_datetime.year)
            month = str(_datetime.month)
            if len(month) == 1:
                month = month.zfill(2)
            current_period = "".join((year, month))
            epd = parser.print_epd(period=current_period)
            if epd is None:
                app.send_message(chat_id=chat_id, text="Файл отсутствует")
            else:
                app.send_document(chat_id=chat_id, document=open(epd, 'rb'))
            return_to_main_menu(message, parser)
        case 'Сменить адрес доставки email':
            msg = app.send_message(chat_id=chat_id,
                                   text="Главное меню",
                                   reply_markup=main_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Сменить пароль':
            msg = app.send_message(chat_id=chat_id,
                                   text="Главное меню",
                                   reply_markup=main_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'История показаний':
            msg = app.send_message(chat_id=chat_id,
                                   text="Главное меню",
                                   reply_markup=main_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Передать показания':
            msg = app.send_message(chat_id=chat_id,
                                   text="Главное меню",
                                   reply_markup=main_menu)
            app.register_next_step_handler(msg, check_menu_btn, parser)
        case 'Назад':
            app.send_message(chat_id=chat_id,
                             text="Главное меню",
                             reply_markup=main_menu)
            return_to_main_menu(message, parser)
        case 'Выход':
            parser.logout()
            del parser
            app.send_message(chat_id=chat_id,
                             text="Закрываем меню",
                             reply_markup=delete_menu)


@app.message_handler(commands=['help'])
def send_help(message: Message):
    app.reply_to(message, "Howdy, how are you doing?")


if __name__ == "__main__":
    app.infinity_polling(skip_pending=True)
