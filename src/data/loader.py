from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import DataBase


bot = Bot('TOKEN_YUMMY_DROP', parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase()

HELP_COMMAND = """
<b>/help</b> - <em>Список команд</em>
<b>/start</b> - <em>Запуск бота</em>
<b>/contact</b> - <em>Связаться с нами</em>
"""