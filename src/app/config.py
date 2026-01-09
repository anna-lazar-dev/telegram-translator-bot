from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    default_target_lang: str = "en"
    translate_provider: str = "yandex"

    # Яндекс переводчик
    yandex_folder_id: str = ""
    yandex_sa_key_file: str = ""


def load_config() -> Config:
    return Config(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        default_target_lang=os.getenv("DEFAULT_TARGET_LANG", "en").strip(),
        translate_provider=os.getenv("TRANSLATE_PROVIDER", "yandex").strip(),
        yandex_folder_id=os.getenv("YANDEX_FOLDER_ID", "").strip(),
        yandex_sa_key_file=os.getenv("YANDEX_SA_KEY_FILE", "").strip(),
    )

