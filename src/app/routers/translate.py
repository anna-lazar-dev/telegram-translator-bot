import asyncio
import json
import time
from pathlib import Path

import httpx
import jwt  # pyjwt
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.app.state import USER_PREFS, UserPrefs
from src.app.config import load_config

router = Router()


def _load_sa_key(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise RuntimeError(f"Файл сервисного аккаунта не найден: {p.resolve()}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _make_jwt(sa_key: dict) -> str:
    """
    Делает JWT для обмена на IAM-токен.
    """
    now = int(time.time())
    payload = {
        "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        "iss": sa_key["service_account_id"],
        "iat": now,
        "exp": now + 3600,
    }

    # В key.json обычно есть 'private_key' и 'id' (key id)
    headers = {"kid": sa_key["id"]}
    token = jwt.encode(payload, sa_key["private_key"], algorithm="PS256", headers=headers)
    # pyjwt может вернуть bytes в старых версиях
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def _get_iam_token_sync(sa_key_file: str) -> str:
    """
    Синхронно получает IAM-токен по authorized_key.json
    """
    sa_key = _load_sa_key(sa_key_file)
    jwt_token = _make_jwt(sa_key)

    r = httpx.post(
        "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        json={"jwt": jwt_token},
        timeout=20,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"IAM token error {r.status_code}: {r.text[:300]}")

    data = r.json()
    return data["iamToken"]


def _translate_sync(folder_id: str, iam_token: str, text: str, target_lang: str) -> str:
    r = httpx.post(
        "https://translate.api.cloud.yandex.net/translate/v2/translate",
        headers={"Authorization": f"Bearer {iam_token}"},
        json={
            "folderId": folder_id,
            "texts": [text],
            "targetLanguageCode": target_lang,
        },
        timeout=20,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Translate error {r.status_code}: {r.text[:300]}")
    data = r.json()
    translations = data.get("translations") or []
    return translations[0].get("text", "") if translations else ""


async def translate_text(text: str, target_lang: str) -> str:
    cfg = load_config()

    if cfg.translate_provider != "yandex":
        return f"[{target_lang}] {text}"

    if not cfg.yandex_folder_id:
        raise RuntimeError("YANDEX_FOLDER_ID не установлен в .env")
    if not cfg.yandex_sa_key_file:
        raise RuntimeError("YANDEX_SA_KEY_FILE не установлен в .env")

    # 1) IAM токен (в отдельном потоке)
    iam_token = await asyncio.to_thread(_get_iam_token_sync, cfg.yandex_sa_key_file)

    # 2) Перевод (в отдельном потоке)
    return await asyncio.to_thread(_translate_sync, cfg.yandex_folder_id, iam_token, text, target_lang)


@router.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery):
    code = callback.data.split(":", 1)[1]
    USER_PREFS[callback.from_user.id] = UserPrefs(target_lang=code)
    await callback.answer(f"Язык перевода: {code}", show_alert=False)
    await callback.message.edit_text(
        f"✅ Язык перевода установлен: {code}\n\nТеперь отправь текст."
    )


@router.message(F.text & ~F.text.startswith("/"))
async def on_text(message: Message):
    text = (message.text or "").strip()
    if not text:
        return

    prefs = USER_PREFS.get(message.from_user.id)
    target = prefs.target_lang if prefs else load_config().default_target_lang

    try:
        result = await translate_text(text, target)
        if not result:
            await message.answer("Не получилось перевести (пустой ответ). Попробуй ещё раз.")
            return
        await message.answer(result)

    except Exception as e:
        await message.answer(
            "Не получилось перевести 😕\n"
            "Попробуй другой текст или чуть позже.\n\n"
            f"Ошибка: {str(e)[:200]}"
        )
