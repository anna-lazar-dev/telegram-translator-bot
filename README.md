# 🤖 Telegram Translator Bot (Yandex Cloud)

Асинхронный Telegram-бот на Python, который переводит любые сообщения на выбранный язык с помощью **Yandex Cloud Translate API**.

---

## ✨ Возможности

- Перевод сообщений в реальном времени
- Выбор языка перевода через кнопки
- Асинхронная архитектура (aiogram 3)
- Подключение к Yandex Cloud через IAM
- Безопасная работа через `.env`

---

## 🛠 Технологии

- Python 3.12
- aiogram 3.x
- httpx
- python-dotenv
- Yandex Cloud Translate API

---

## 🚀 Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/<your-username>/telegram-translator-bot
cd telegram-translator-bot
````

### 2. Установить зависимости

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

### 3. Создать .env

Создать .env

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

И заполните своими ключами:
BOT_TOKEN=...
TRANSLATE_PROVIDER=yandex
YANDEX_FOLDER_ID=...
YANDEX_SA_KEY_FILE=authorized_key.json

### 4. Запуск

Запуск

📌 Команды бота

| Команда     | Описание    |
| ----------- | ----------- |
| /start      | Запуск бота |
| /lang       | Выбор языка |
| Любой текст | Перевод     |

👩‍💻 Автор

Anna Lazar
Telegram: @your_username
2026

