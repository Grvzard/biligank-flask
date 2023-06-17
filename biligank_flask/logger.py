import json
from pathlib import Path

import pymongo
import requests

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


def make_logs_dir():
    Path('logs').mkdir(exist_ok=True)


class JsonLogger:
    def __init__(self, file_name):
        make_logs_dir()
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


class TgbotLogger:
    HTML_ENTITIES = (
        ('<', '&lt;'),
        ('>', '&gt;'), 
        ('&', '&amp;')
    )

    def __init__(self, setting):
        self.token = setting['token']
        self.chat_id = setting['chat_id']

    def log(self, log_info):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        text = "#biligank-logger\n"
        text += "\n".join(map(str, log_info.values()))

        for _ in self.HTML_ENTITIES:
            text = text.replace(_[0], _[1])
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            'disable_web_page_preview': True,
        }
        resp = requests.post(url, json=payload, timeout=5).json()
        if resp['ok']:
            return True
        else:
            raise Exception(
                'tgbot send msg failed: [%s] %s'
                % (resp['result']['error_code'], resp['result']['description'])
            )
