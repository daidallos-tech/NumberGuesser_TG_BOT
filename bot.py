import asyncio
from aiogram import Bot, Dispatcher
from commands import user_router
from game import game_router

BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(game_router)
dp.include_router(user_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


