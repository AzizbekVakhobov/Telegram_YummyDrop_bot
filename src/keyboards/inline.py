from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db


def generate_main_inline_menu():
    markup = InlineKeyboardMarkup()
    catalog_btn = InlineKeyboardButton('🛍 Каталог', callback_data='catalog')
    cart_btn = InlineKeyboardButton('🛒 Корзина', callback_data='cart')
    feedback_btn = InlineKeyboardButton('✍ Оставить отзыв', callback_data='feedback')
    info_btn = InlineKeyboardButton('ℹ О нас', callback_data='info')
    settings_btn = InlineKeyboardButton('⚙ Настройки', callback_data='settings')
    markup.add(catalog_btn)
    markup.add(info_btn, cart_btn)
    markup.add(feedback_btn, settings_btn)
    return markup


def generate_catalog_inline():
    markup = InlineKeyboardMarkup()
    main_menu_btn = InlineKeyboardButton('◀ Главное меню', callback_data='main_menu')
    categories = [i[0] for i in db.get_categories()]
    buttons = []
    for category in categories:
        btn = InlineKeyboardButton(text=category, callback_data=f'{category}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(main_menu_btn)
    return markup

def generate_settings_inline():
    markup = InlineKeyboardMarkup()
    main_menu_btn = InlineKeyboardButton('◀ Главное меню', callback_data='main_menu')
    user_info = InlineKeyboardButton('Личная информация', callback_data='personal_info')
    markup.row(user_info)
    markup.row(main_menu_btn)
    return markup

def generate_products(category_title):
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('◀ К категориям', callback_data='back_to_categories')
    cart = InlineKeyboardButton('🛒 Корзина', callback_data='cart')
    main_btn = InlineKeyboardButton('◀ Главное меню', callback_data='main_menu')
    products = [i[0] for i in db.get_products_by_category(category_title)]
    buttons = []
    for product in products:
        btn = InlineKeyboardButton(text=product, callback_data=f'{product}')
        buttons.append(btn)
    markup.row(cart)
    markup.add(*buttons)
    markup.row(back_btn, main_btn)
    return markup


def generate_product_detail(product_id, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_btn = InlineKeyboardButton('➖', callback_data='minus')
    quan_btn = InlineKeyboardButton(str(quantity), callback_data=f'quantity_{product_id}')
    plus_btn = InlineKeyboardButton('➕', callback_data='plus')
    buy_btn = InlineKeyboardButton('🛒 Добавить в корзину', callback_data=f'add_{product_id}_{quantity}')
    back_btn = InlineKeyboardButton('◀ Главное меню', callback_data='main_menu')
    markup.add(minus_btn, quan_btn, plus_btn)
    markup.add(buy_btn)
    markup.add(back_btn)
    return markup


def generate_cart_buttons(cart_products, cart_id):
    markup = InlineKeyboardMarkup()
    for cart_product in cart_products:
        name = InlineKeyboardButton(text=cart_product[2], callback_data='name')
        markup.row(name)

    clear = InlineKeyboardButton(text='Очистить', callback_data='clear')
    order = InlineKeyboardButton(text='Купить', callback_data=f'order_{cart_id}')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(clear, order)
    markup.row(main_menu)
    return markup
