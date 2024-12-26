import logging
import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class BotConfig:
    api_token: str


@dataclass
class Application:
    host: str
    port: str
    secret_key: str


@dataclass
class DbConfig:
    host: str
    port: str
    username: str
    password: str
    database: str


@dataclass
class OtherConfig:
    dns_name: str


@dataclass
class Config:
    bot: BotConfig
    app: Application
    database: DbConfig
    other: OtherConfig


def load_config() -> Config:
    load_dotenv()

    api_token: str = os.getenv("API_TOKEN")

    application_host: str = os.getenv("APP_HOST")
    application_port: str = os.getenv("APP_PORT")
    application_secret_key: str = os.getenv("APP_SECRET_KEY")

    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_username: str = os.getenv("DB_USERNAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_database: str = os.getenv("DB_DATABASE")

    dns_name: str = os.getenv("DNS_NAME")

    return Config(
        bot=BotConfig(api_token=api_token),
        app=Application(
            host=application_host,
            port=application_port,
            secret_key=application_secret_key,
        ),
        database=DbConfig(
            host=db_host,
            port=db_port,
            username=db_username,
            password=db_password,
            database=db_database
        ),
        other=OtherConfig(
            dns_name=dns_name,
        )
    )
