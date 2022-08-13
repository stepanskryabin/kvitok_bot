import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton

from src.settings.config import TELEGRAM_TOKEN
from src.parser.manager import Parser
from src.parser.models import UserInformation
from src.parser.manager import LoginError


app = telebot.TeleBot(token=TELEGRAM_TOKEN,
                      parse_mode=None)


@app.message_handler(commands=['start'])
def send_start(message: Message):
    msg = app.reply_to(message, "Введите номер лицевого счёта:")
    app.register_next_step_handler(msg, check_username)
    app.enable_save_next_step_handlers(delay=2)
    app.load_next_step_handlers()


def check_username(message: Message):
    username = str(message.text)
    letters = len(list(message.text))
    if username.isnumeric() and letters == 5:
        msg = app.reply_to(message, "Введите пароль:")
        app.register_next_step_handler(msg, check_password, username)


def check_password(message: Message, username: str):
    password = message.text
    parser = Parser(username=username, password=password)

    menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    user_info = KeyboardButton('Информация')
    pays_info = KeyboardButton('Платежи')
    epd = KeyboardButton('Квитанция')
    log_out = KeyboardButton('Выход')
    menu.add(user_info, pays_info, epd, log_out)

    try:
        parser.login()
    except LoginError:
        msg = app.reply_to(message,
                           "Номер л/с или пароль не верные. Введите л/с заново:")
        app.register_next_step_handler(msg, check_username)
    else:
        msg = app.reply_to(message,
                           "Авторизация прошла успешно!.",
                           reply_markup=menu)
        app.register_next_step_handler(msg, main_menu, parser)


def main_menu(message: Message, parser: Parser):
    menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    user_info = KeyboardButton('Информация')
    pays_info = KeyboardButton('Платежи')
    epd = KeyboardButton('Квитанция')
    log_out = KeyboardButton('Выход')
    menu.add(user_info, pays_info, epd, log_out)
    app.register_next_step_handler(message,
                                   check_menu_btn,
                                   parser=parser,
                                   menu=menu)


def return_menu(message: Message, parser: Parser, menu: ReplyKeyboardMarkup):
    # msg = app.reply_to(message, "Выберите пункт меню", reply_markup=menu)
    app.register_next_step_handler(message,
                                   check_menu_btn,
                                   parser=parser,
                                   menu=menu)


def check_menu_btn(message: Message,
                   parser: Parser,
                   menu: ReplyKeyboardMarkup):
    chat_id = message.chat.id
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
            """
            app.send_message(chat_id=chat_id, text=info)
            return_menu(message, parser, menu)
        case 'Платежи':
            pay_history = parser.pays_history(date_start="01.01.2022",
                                              date_stop="01.08.2022")
            for pay in pay_history:
                msg = f"{pay.data_income} - {pay.amount} - {pay.pay_agent}"
                app.send_message(chat_id=chat_id, text=msg)
            return_menu(message, parser, menu)
        case 'Квитанция':
            epd = parser.print_epd(period="202206")
            if epd is None:
                app.send_message(chat_id=chat_id, text="Файл отсутствует")
            else:
                app.send_document(chat_id=chat_id, document=open(epd, 'rb'))
            return_menu(message, parser, menu)
        case 'Выход':
            parser.logout()
            del_menu = ReplyKeyboardRemove()
            app.send_message(chat_id=chat_id,
                             text="Закрываем меню",
                             reply_markup=del_menu)
        case _:
            return_menu(message, parser, menu)


@app.message_handler(commands=['help'])
def send_help(message: Message):
    app.reply_to(message, "Howdy, how are you doing?")


if __name__ == "__main__":
    app.infinity_polling()
