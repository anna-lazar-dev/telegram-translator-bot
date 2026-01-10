from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# код -> (название, флаг)
LANGS = {
    "en": ("English", "🇬🇧"),
    "ru": ("Русский", "🇷🇺"),
    "de": ("Deutsch", "🇩🇪"),
    "fr": ("Français", "🇫🇷"),
    "es": ("Español", "🇪🇸"),
    "it": ("Italiano", "🇮🇹"),
    "tr": ("Türkçe", "🇹🇷"),
    "ar": ("العربية", "🇸🇦"),
    "zh": ("中文", "🇨🇳"),
    "uk": ("Українська", "🇺🇦"),
}

def lang_label(code: str) -> str:
    name, flag = LANGS.get(code, (code.upper(), "🏳️"))
    return f"{flag} {name} ({code})"

def lang_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    # раскладка по 2 кнопки в ряд
    for code in LANGS.keys():
        kb.button(text=lang_label(code), callback_data=f"lang:{code}")

    kb.adjust(2)
    return kb.as_markup()