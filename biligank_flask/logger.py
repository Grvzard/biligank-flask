import time
from copy import deepcopy

import pymongo
import requests

from biligank_flask.utils import get_clock, get_date, write_json

__all__ = 'SearchLogger', 'FeedbackLogger',


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
            self.loggers.append(h)


class FeedbackLogger(MultiLogger):
    def log(self, data):
        log_info = deepcopy(data)
        for logger in self.loggers:
            logger.log(log_info)


class SearchLogger(MultiLogger):
    def log(self, **records):
        log_info = deepcopy(records)
        log_info['ts'] = int(time.time())
        log_info['clock'] = get_clock()

        for logger in self.loggers:
            logger.log(log_info)


class JsonLogger:
    def __init__(self, file_name):
        self.file_name = file_name

    def log(self, log_info):
        write_json(log_info, self.file_name)


class MongoLogger:
    def __init__(self, setting):
        self.mongo_client: pymongo.MongoClient = pymongo.MongoClient(setting['config'])
        self.db = self.mongo_client[setting['db']]

    def log(self, log_info):
        self.db[get_date()].insert_one(log_info)


class TgbotLogger:
    def __init__(self, setting):
        self.token = setting['token']
        self.chat_id = setting['chat_id']
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def log(self, log_info):
        text = ""
        for k, v in log_info.items():
            text += f"{v}\n"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
        resp = requests.post(self.url, json=payload, timeout=3).json()
        if resp['ok']:
            return True
        else:
            raise Exception('tgbot send msg failed')
