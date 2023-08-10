import json
from pathlib import Path
from typing import Final, Dict

import pymongo
import httpx
from pydantic import BaseModel

from .utils import get_date

__all__ = 'MultiLogger', 'JsonLogger', 'MongoLogger', 'TgbotLogger'


class MultiLogger:
    def __init__(self, **loggers):
        self.loggers = []
        for type_, setting in loggers.items():
            if type_.startswith('mongo'):
                h = MongoLogger(setting)
            elif type_.startswith('json'):
                h = JsonLogger(setting)
            elif type_.startswith('tgbot'):
                h = TgbotLogger(setting)
            else:
                raise Exception('unknown logger type')
            self.loggers.append(h)

    def log(self, log_info):
        for logger in self.loggers:
            logger.log(log_info)


class JsonLogger:
    def __init__(self, file_name):
        Path('logs').mkdir(exist_ok=True)
        self.file = Path('logs') / file_name

    def log(self, log_info):
        with self.file.open('a', encoding='utf-8') as f:
            json.dump(log_info, f, ensure_ascii=False, indent=4)
            f.write(',')


class MongoLogger:
    def __init__(self, setting):
        self.mongo_client: pymongo.MongoClient = pymongo.MongoClient(setting['config'])
        self.db = self.mongo_client[setting['db']]

    def log(self, log_info):
        self.db[get_date()].insert_one(log_info)


class TgbotConfig(BaseModel):
    token: str
    chat_id: str
    tag_prefix: str = 'biligank'
    proxy: str = ''


class TgbotLogger:
    HTML_ENTITIES: Final[Dict[str, str]] = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
    }

    def __init__(self, setting: dict):
        self._config = TgbotConfig(**setting)
        self._proxies = {}
        if self._config.proxy:
            self._proxies['https://'] = self._config.proxy

    def log(self, log_info):
        url = f"https://api.telegram.org/bot{self._config.token}/sendMessage"

        word_list = []
        for info in log_info.values():
            i = str(info)
            for c in i:
                if (r := self.HTML_ENTITIES.get(c, None)):
                    word_list.append(r)
                else:
                    word_list.append(c)
            word_list.append('\n')

        text = f"#{self._config.tag_prefix}\n" + ''.join(word_list)

        payload = {
            "chat_id": self._config.chat_id,
            "text": text,
            "parse_mode": "HTML",
            'disable_web_page_preview': True,
        }

        resp = httpx.post(url, json=payload, timeout=10, proxies=self._proxies).json()

        if resp['ok']:
            return True
        else:
            raise Exception(
                'tgbot send msg failed: [%s] %s'
                % (resp['result']['error_code'], resp['result']['description'])
            )
