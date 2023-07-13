from data.loader import db, dp, bot
from aiogram.types import CallbackQuery, LabeledPrice, ShippingOption
from keyboards.inline import generate_catalog_inline, generate_main_inline_menu, generate_settings_inline, \
    generate_products, generate_product_detail, generate_cart_buttons
from keyboards.reply import come_back_button, accept_settings_pers_inf, generate_main_menu_button
from handlers.text_handlers import feedback_register, show_product_detail
from aiogram.types import Message
from database.database import combine_functions

@dp.callback_query_handler(lambda call: 'catalog' == call.data)
async def reaction_to_catalog(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = 'https://telegra.ph/Menyu-07-05-10'
    await bot.send_message(chat_id, text,
                           reply_markup=generate_catalog_inline())


@dp.callback_query_handler(lambda call: 'main_menu' == call.data)
async def reaction_to_back_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id, f'Не забудьте оставить отзыв 🤗', reply_markup=generate_main_menu_button())
    await bot.send_message(chat_id, 'https://telegra.ph/Menyu-07-05-10', reply_markup=generate_main_inline_menu())
    await call.message.delete()


@dp.callback_query_handler(lambda call: 'info' == call.data)
async def reaction_to_info_btn(call: CallbackQuery):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id, f'YummyDrop, ваш интернет-магазин сладостей, основанный Вахобовым Азизбеком. '
                                    f'Мы предлагаем широкий выбор аппетитных угощений, от леденцов до мармелада, от выпечки до конфет. '
                                    f'Независимо от того, чего жаждет ваш внутренний сладкоежка, YummyDrop может предоставить. '
                                    f'Затеряйтесь в разнообразии нашего ассортимента и насладитесь сладостью наших угощений вместе с YummyDrop!',
                           reply_markup=generate_main_menu_button())
    await bot.send_message(chat_id, 'https://telegra.ph/Menyu-07-05-10')
    await call.message.delete()


@dp.callback_query_handler(lambda call: 'feedback' == call.data)
async def reaction_to_feedback(call: CallbackQuery):
    chat_id = call.message.chat.id
    message = Message()
    text = 'Отправьте ваш отзыв ✍'
    await bot.send_message(chat_id, text, reply_markup=come_back_button())
    await feedback_register(message)


@dp.callback_query_handler(lambda call: 'settings' == call.data)
async def reaction_to_settings(call: CallbackQuery):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id, '\n\n\nВыберете одно из следующих\n\n\n', reply_markup=generate_settings_inline())
    await call.message.delete()


@dp.callback_query_handler(lambda call: 'personal_info' == call.data)
async def reaction_to_personal_info(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = 'Хотите что то изменить?'
    user = db.get_user_by_id(chat_id)
    await bot.send_message(chat_id, f'И.Ф: {user[1]}'
                                    f'\n\nНомер телефона: {user[2]}'
                                    f'\n\nДата рождения: {user[3]}'
                                    f'\n\nВсе верно?', reply_markup=accept_settings_pers_inf())
    await call.message.delete()


categories = [i[0] for i in db.get_categories()]


@dp.callback_query_handler(lambda call: call.data in categories)
async def reaction_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = 'https://telegra.ph/Menyu-07-05-10'
    await bot.send_message(chat_id, f'{call.from_user.full_name} оформим ваш заказ вместе?🤗')
    await bot.send_message(chat_id, text)
    await bot.send_message(chat_id, 'Выберите товар: ', reply_markup=generate_products(call.data))
    await call.message.delete()


products = [i[0] for i in db.get_all_products()]


@dp.callback_query_handler(lambda call: call.data in products)
async def show_product_details(call: CallbackQuery):
    chat_id = call.message.chat.id
    product = db.get_product_by_title(call.data)
    with open(product[4], mode='rb') as photo:
        caption = f'Товар: {product[1]}\n\n{product[2]}\n\nЦена {product[3]}сум'
        await bot.send_photo(chat_id,
                             photo=photo,
                             caption=caption,
                             reply_markup=generate_product_detail(product[0]))


@dp.callback_query_handler(lambda call: call.data == 'plus')
async def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity < 5:
        quantity += 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_detail(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Вы не можете купить больше 5 товаров одного наименования')


@dp.callback_query_handler(lambda call: call.data == 'minus')
async def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    buttons = call.message.reply_markup.inline_keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[0][1].callback_data.split('_')[1]
    if quantity > 1:
        quantity -= 1
        await bot.edit_message_reply_markup(chat_id, message_id,
                                            reply_markup=generate_product_detail(product_id, quantity))
    else:
        await bot.answer_callback_query(call.id,
                                        'Нельзя купить менее 1 товара')


@dp.callback_query_handler(lambda call: 'add' in call.data)
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')[0:3]
    product_id, quantity = int(product_id), int(quantity)
    product_title, price = db.get_product_by_id(product_id)
    final_price = quantity * price
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    try:
        '''Пытаемся закинуть новый товар в корзину'''
        db.insert_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Товар успешно добавлен в корзину''')

    except:
        '''Если такой товар был, то обновляем его кол-во и цену'''
        db.update_cart_product(cart_id, product_title, quantity, final_price)
        await bot.answer_callback_query(call.id, '''Количество успешно изменено''')


@dp.callback_query_handler(lambda call: 'cart' == call.data)
async def show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    if db.get_cart_id(chat_id):
        cart_id = db.get_cart_id(chat_id)[0]
    else:
        db.create_cart_for_user(chat_id)
        cart_id = db.get_cart_id(chat_id)[0]

    db.update_cart_total_price_quantity(cart_id)
    total_price, total_quantity = db.get_cart_total_price_quantity(cart_id)
    try:
        total_price, total_quantity = int(total_price), int(total_quantity)
    except:
        total_price, total_quantity = 0, 0
    cart_products = db.get_cart_products_by_cart_id(cart_id)

    text = '''Ваша корзина: \n\n'''
    print(total_price, total_quantity, cart_products)
    for cart_product in cart_products:
        text += f'{cart_product[2]} - {cart_product[4]} шт - {cart_product[3]} сум\n\n'

    text += f'''Общее количество: {total_quantity} шт
Общая стоимость: {total_price} сум'''
    await bot.send_message(chat_id, text,
                           reply_markup=generate_cart_buttons(cart_products, cart_id))
    await call.message.delete()



@dp.callback_query_handler(lambda call: 'clear' == call.data)
async def clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    combine_functions(chat_id)
    await bot.answer_callback_query(call.id, '''Корзина очищена''')
    await bot.send_message(chat_id, 'https://telegra.ph/Menyu-07-05-10', reply_markup=generate_main_inline_menu())
    await call.message.delete()


@dp.callback_query_handler(lambda call: 'order' in call.data)
async def payment(call: CallbackQuery):
    chat_id = call.message.chat.id
    cart_id = call.data.split('_')[1]
    products_cart = db.get_cart_products_by_cart_id(cart_id)

    await bot.send_invoice(chat_id=chat_id,
                           title=f'Чек для {call.message.from_user.full_name}',
                           description=''.join([f'{product[2]}\n' for product in products_cart]),
                           payload='YummyDrop',
                           start_parameter='create_invoice_products',
                           currency='UZS',
                           prices=[
                               LabeledPrice(
                                   label=f'{product[2]} - {product[4]} шт',
                                   amount= int(product[3] * 100)
                               ) for product in products_cart
                           ],
                           provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                           need_name=True,
                           need_shipping_address=True,
                           is_flexible=True
                           )
    await call.message.delete()




EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='До 40 мин'
).add(LabeledPrice(label='До 40 мин', amount=30_000_00))


REGULAR_SHIPPING = ShippingOption(
    id='post_regular',
    title='Самовывоз'
).add(LabeledPrice(label='Самовывоз', amount=0))


@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query):
    await bot.answer_shipping_query(shipping_query.id,
                                    ok=True,
                                    shipping_options=[EXPRESS_SHIPPING, REGULAR_SHIPPING],
                                    error_message='Простите что то не так')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre):
    await bot.answer_pre_checkout_query(pre.id,
                                        ok=True,
                                        error_message='Опять что то не так')



@dp.message_handler(content_types=['successful_payment'])
async def success(message):
    await bot.send_message(message.chat.id, 'Ура! Оплата прошла успешно!')