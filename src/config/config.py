import logging
import os

from dataclasses import dataclass


@dataclass
class BotConfig:
    """Bot config"""

    api_token: str


@dataclass
class Config:
    """App config"""

    bot: BotConfig


def load_config() -> Config:
    """Get app config"""

    api_token: str = os.environ["API_TOKEN"]

    return Config(
        bot=BotConfig(api_token=api_token),
    )
