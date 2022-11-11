"""Loads configuration data to share"""

import configparser
from dataclasses import dataclass


@dataclass(frozen=True)
class Bot:
    API_TOKEN: str


@dataclass(frozen=True)
class DB:
    DSN: str


@dataclass(frozen=True)
class MainConf:
    """All configs composition"""
    db: DB
    bot: Bot


def read_config(conf_path: str) -> MainConf:
    """Gets .ini into config object"""
    conf = configparser.ConfigParser()
    conf.read(conf_path)

    db = conf['db']
    bot = conf['bot']

    return MainConf(
        DB(db.get('DSN')),
        Bot(bot.get('API_TOKEN'))
    )
