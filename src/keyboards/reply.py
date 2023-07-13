from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db


def generate_main_menu_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = KeyboardButton(text='🏠 Главное меню')
    markup.row(main_menu)
    return markup


def accept_registration_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    yes_btn = KeyboardButton(text='Да')
    no_btn = KeyboardButton(text='Нет')
    markup.row(yes_btn, no_btn)
    return markup

def accept_settings_pers_inf():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    yes_btn = KeyboardButton(text='Изменить')
    no_btn = KeyboardButton(text='Оставить как есть')
    markup.row(yes_btn, no_btn)
    return markup

def come_back_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    come_back_btn = KeyboardButton(text='◀ Назад')
    markup.row(come_back_btn)
    return markup


# def phone_btn():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True)
#     phone_btn = KeyboardButton(text='📞 Отправить номер телефона', request_contact=True)
#     markup.row(phone_btn)
#     return markup
