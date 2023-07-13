from data.loader import dp, executor
import handlers


async def on_startup(_):
    print('Бот успешно запущен!')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

