from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LANGS = [
    ("English", "en"),
    ("Русский", "ru"),
    ("Deutsch", "de"),
    ("Français", "fr"),
    ("Español", "es"),
    ("Türkçe", "tr"),
    ("Українська", "uk"),
]

def lang_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"lang:{code}")]
        for name, code in LANGS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
