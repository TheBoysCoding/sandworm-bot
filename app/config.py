__all__ = ("config")

from configparser import ConfigParser
from dataclasses import dataclass

from .args import args

@dataclass
class TelegramConfig:
    token: str
    chats: list[int] = None

@dataclass
class CameraConfig:
    device: str = None

@dataclass
class Config:
    telegram: TelegramConfig
    camera: CameraConfig
    stickers: dict[str, str]

def parse_chats(value: str) -> list[int]:
    if str is None:
        return None
    return [int(chat_id) for chat_id in value.split(', ')]

def load_config() -> Config:
    parser = ConfigParser()
    parser.read(args.config)

    config = Config(
        telegram = TelegramConfig(
            token = parser.get("telegram", "token"),
            chats = parse_chats(parser.get("telegram", "chats", fallback=None))
        ),
        camera = CameraConfig(
            device = parser.get("camera", "device", fallback=None)
        ),
        stickers = {
            key: value for key, value in parser.items("stickers")
        }
    )

    return config

config = load_config()
