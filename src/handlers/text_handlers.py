from aiogram.dispatcher.storage import FSMContext
from states.states import NumberState, FullNameState, BirthState, FeedbackState
from aiogram.types import Message
from data.loader import bot, dp, db
import re
from keyboards.reply import generate_main_menu_button, accept_registration_button
from database.database import DataBase
from keyboards.inline import generate_main_inline_menu, generate_catalog_inline, generate_settings_inline, generate_product_detail


async def name_register(message: Message, state=None):
    await FullNameState.fullname.set()
    await message.answer('\n\nДля начало вам нужно пройти <u>регистрацию</u>'
                         '\n\n<b>Введите ваше И.Ф как на примере:</b> <u>Антон Павлов</u>', parse_mode="HTML",
                         reply_markup=generate_main_menu_button())


@dp.message_handler(state=FullNameState.fullname)
async def get_name(message: Message, state: FSMContext):
    fullname = message.text
    if fullname:
        await state.finish()
        chat_id = message.chat.id
        db.insert_user_fullname(chat_id, fullname)
        await phone_register(message)


async def phone_register(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('Введите номер телефона в формате: +998 ** *** ** **')


@dp.message_handler(state=NumberState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text
    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', phone)
    result2 = re.search(r'\+998\d{9}', phone)
    if result1 or result2:
        await state.finish()
        chat_id = message.chat.id
        db.add_user_phone(phone, chat_id)
        '''Регистрация даты рождения'''
        await birth_register(message)
    else:
        await state.finish()
        await again_ask_phone(message)


async def again_ask_phone(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('''Не верный формат телефона.
Введите номер телефона в формате: +998 ** *** ** **''')


async def birth_register(message: Message, state=None):
    await BirthState.birth.set()
    await message.answer('Введите дату рождения в формате: ДДММГГГГ')


@dp.message_handler(state=BirthState.birth)
async def get_birth_date(message: Message, state: FSMContext):
    birth = message.text
    result1 = re.search(r'\d\d\d\d\d\d\d\d', birth)
    result2 = re.search(r'\d{8}', birth)
    if result1 or result2:
        await state.finish()
        chat_id = message.chat.id
        db.add_user_date_of_birth(birth, chat_id)
        '''Показать главное меню'''
        await check_for_errors(message)
    else:
        await state.finish()
        await again_ask_birth_date(message)


async def again_ask_birth_date(message: Message, state=None):
    await BirthState.birth.set()
    await message.answer('''Не верный формат даты рождения.
Введите дату рождения в формате: ДДММГГГГ''')


@dp.message_handler(regexp='🏠 Главное меню')
async def show_main_menu(message: Message):
    chat_id = message.chat.id
    user = db.get_user_by_id(chat_id)
    if user:
        '''
        Показать главное меню
        '''
        await bot.send_message(chat_id, f'{message.chat.first_name} оформим ваш заказ вместе?🤗',
                               reply_markup=generate_main_menu_button())
        await message.answer('https://telegra.ph/Menyu-07-05-10', reply_markup=generate_main_inline_menu())
    else:
        await name_register(message)


async def check_for_errors(message: Message):
    chat_id = message.chat.id
    user = db.get_user_by_id(chat_id)
    await bot.send_message(chat_id, f'И.Ф: {user[1]}'
                                    f'\n\nНомер телефона: {user[2]}'
                                    f'\n\nДата рождения: {user[3]}'
                                    f'\n\nВсе верно?', reply_markup=accept_registration_button())


@dp.message_handler(regexp='Да')
async def complete_registration(message: Message):
    await show_main_menu(message)\


@dp.message_handler(regexp='Нет')
async def repeat_registration(message: Message):
    chat_id = message.chat.id
    db.clean_users_data(chat_id)
    await name_register(message)

@dp.message_handler(regexp='Изменить')
async def change_info_in_settings(message: Message):
    chat_id = message.chat.id
    db.clean_users_data(chat_id)
    await name_register(message)


@dp.message_handler(regexp='Оставить как есть')
async def dont_change_info_in_settings(message: Message):
    await message.answer('\n\n\nВыберете одно из следующих\n\n\n', reply_markup=generate_settings_inline())


async def show_catalog(message: Message):
    await message.answer('https://telegra.ph/Menyu-07-05-10', reply_markup=generate_catalog_inline())


@dp.message_handler(regexp='◀ Назад')
async def come_back_func(message: Message):
    await show_main_menu(message)


async def feedback_register(message: Message, state=None):
    await FeedbackState.feedback.set()


@dp.message_handler(state=FeedbackState.feedback)
async def get_feedback(message: Message, state: FSMContext):
    await show_main_menu(message)


products = [i[0] for i in db.get_all_products()]

@dp.message_handler(lambda message: message.text in products)
async def show_product_detail(message: Message):
    product = db.get_product_by_title(message.text)
    with open(product[4], mode='rb') as photo:
        caption = f'Товар: {product[1]}\n\n{product[2]}\n\nЦена {product[3]}сум'
        await bot.send_photo(message.chat.id,
                             photo=photo,
                             caption=caption,
                             reply_markup=generate_product_detail(product[0]))