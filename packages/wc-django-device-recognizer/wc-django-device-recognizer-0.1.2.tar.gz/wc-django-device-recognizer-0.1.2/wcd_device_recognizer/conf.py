from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


@s('WCD_DEVICE_RECOGNIZER')
@dataclass
class Settings:
    pass


settings = Settings()
