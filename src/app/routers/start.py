from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.app.keyboards import lang_keyboard
from src.app.state import USER_PREFS, UserPrefs
from src.app.config import load_config


router = Router()


@router.message(Command("start"))
async def start(message: Message):
    cfg = load_config()
    USER_PREFS[message.from_user.id] = UserPrefs(target_lang=cfg.default_target_lang)

    await message.answer(
        "Привет! Я бот-переводчик.\n\n"
        "1) Выбери язык перевода кнопкой ниже\n"
        "2) Просто отправь текст — я переведу\n\n"
        "Команда: /lang — сменить язык",
        reply_markup=lang_keyboard(),
    )


@router.message(Command("lang"))
async def lang(message: Message):
    await message.answer("Выбери язык перевода:", reply_markup=lang_keyboard())
