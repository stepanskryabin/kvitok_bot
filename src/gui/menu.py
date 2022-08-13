from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
from telebot.types import KeyboardButton


agree_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
am_btn1 = KeyboardButton('Согласен')
am_btn2 = KeyboardButton('Не согласен')
agree_menu.add(am_btn1, am_btn2)

company_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
cm_btn1 = KeyboardButton('ТСО Зиновы')
cm_btn2 = KeyboardButton('УК Чепецкая')
cm_btn3 = KeyboardButton('УК Боёвская')
cm_btn4 = KeyboardButton('Выход')
company_menu.add(cm_btn1, cm_btn2, cm_btn3, cm_btn4)


main_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
mm_btn1 = KeyboardButton('Информация')
mm_btn2 = KeyboardButton('Платежи')
mm_btn3 = KeyboardButton('Счётчики')
mm_btn4 = KeyboardButton('Квитанции')
mm_btn5 = KeyboardButton('Настройки')
mm_btn6 = KeyboardButton('Выход')
main_menu.add(mm_btn1, mm_btn2, mm_btn3, mm_btn4, mm_btn5, mm_btn6)

info_menu = ReplyKeyboardMarkup()
im_btn1 = KeyboardButton('')
info_menu.add(im_btn1)

pay_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pm_btn1 = KeyboardButton('Текущая история')
pm_btn2 = KeyboardButton('Ввести период')
pm_btn3 = KeyboardButton('Назад')
pay_menu.add(pm_btn1, pm_btn2, pm_btn3)

ipu_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
im_btn1 = KeyboardButton('История показаний')
im_btn2 = KeyboardButton('Передать показания')
im_btn3 = KeyboardButton('Назад')
ipu_menu.add(im_btn1, im_btn2, im_btn3)

epd_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
em_btn1 = KeyboardButton('Текущая квитанция')
em_btn2 = KeyboardButton('Ввести период')
em_btn3 = KeyboardButton('Назад')
epd_menu.add(em_btn1, em_btn2, em_btn3)

settings_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
sm_btn1 = KeyboardButton('Сменить адрес доставки email')
sm_btn2 = KeyboardButton('Сменить пароль')
sm_btn3 = KeyboardButton('Назад')
settings_menu.add(sm_btn1, sm_btn2, sm_btn3)

delete_menu = ReplyKeyboardRemove()
