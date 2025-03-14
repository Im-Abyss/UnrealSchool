import asyncio
from aiogram import Bot, Dispatcher


from config import TOKEN
from app.handlers import router
from app.admin import admin


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    dp.include_router(admin)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Бот остановлен")