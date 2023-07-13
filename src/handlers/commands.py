from aiogram.types import Message
from data.loader import bot, dp, db, HELP_COMMAND
from keyboards.reply import generate_main_menu_button
from keyboards.inline import generate_main_inline_menu
@dp.message_handler(commands=['start'])
async def start_message(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'{message.chat.first_name} добро пожаловать в YummyDrop, ваш интернет-магазин сладостей, основанный Вахобовым Азизбеком. '
                                    f'Мы предлагаем широкий выбор аппетитных угощений, от леденцов до мармелада, от выпечки до конфет. '
                                    f'Независимо от того, чего жаждет ваш внутренний сладкоежка, YummyDrop может предоставить. '
                                    f'Затеряйтесь в разнообразии нашего ассортимента и насладитесь сладостью наших угощений вместе с YummyDrop!',
                           reply_markup=generate_main_menu_button())
    await message.answer('https://telegra.ph/Menyu-07-05-10')


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.reply(text=HELP_COMMAND, parse_mode="HTML")


@dp.message_handler(commands=['contact'])
async def command_feedback(message: Message):
    await message.answer('<b>Единый call-center:</b> 1234 или +998(70) 123-45-67')