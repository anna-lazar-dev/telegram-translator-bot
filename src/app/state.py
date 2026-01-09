from dataclasses import dataclass
from typing import Dict


@dataclass
class UserPrefs:
    target_lang: str


# user_id -> prefs
USER_PREFS: Dict[int, UserPrefs] = {}
