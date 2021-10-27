__all__ = ("config")

from configparser import ConfigParser
from dataclasses import dataclass
from typing import List, Dict

from .args import args

@dataclass
class TelegramConfig:
    token: str
    chats: List[int] = None

@dataclass
class JPEGStream:
    url: str = None

@dataclass
class Moonraker:
    url: str = None

@dataclass
class Config:
    telegram: TelegramConfig
    jpeg_stream: JPEGStream
    moonraker: Moonraker
    stickers: Dict[str, str]

def parse_chats(value: str) -> List[int]:
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
        jpeg_stream = JPEGStream(
            url = parser.get("jpeg_stream", "url", fallback=None)
        ),
        moonraker = Moonraker(
            url = parser.get("moonraker", "url", fallback=None)
        ),
        stickers = {
            key: value for key, value in parser.items("stickers")
        }
    )

    return config

config = load_config()
