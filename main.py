#6534235155:AAGdLW-tyZ2e6Uk2_L_xBmGE5cOee9GhUa0
import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import simp_front

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6534235155:AAGdLW-tyZ2e6Uk2_L_xBmGE5cOee9GhUa0")

async def main():

    dp = Dispatcher()
    dp.include_routers(simp_front.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())