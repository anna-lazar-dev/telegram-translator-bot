import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.app.config import load_config
from src.app.routers import all_routers


async def main():
    logging.basicConfig(level=logging.INFO)

    cfg = load_config()
    if not cfg.bot_token:
        raise RuntimeError("BOT_TOKEN is missing. Check .env file.")

    bot = Bot(token=cfg.bot_token)
    dp = Dispatcher()

    for r in all_routers:
        dp.include_router(r)

    me = await bot.get_me()
    logging.info("Bot started: @%s", me.username)

    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    asyncio.run(main())
