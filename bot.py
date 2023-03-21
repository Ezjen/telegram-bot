from aiogram import Bot, Dispatcher, Router
import logging
import asyncio
from config_reader import config
from handlers import questions

bot = Bot(token=config.API_TOKEN.get_secret_value())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=config.API_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(questions.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
