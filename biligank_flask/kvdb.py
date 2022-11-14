from typing import Any

import pymongo


class KvDb:
    def __init__(self, app = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        config = app.config['KV_DB'] and app.config['KV_DB']['config']
        if config:
            client = pymongo.MongoClient(config)
            self.coll = client['biligank_web']['var']

        self._available = bool(config)

        app.extensions['kvdb'] = self

    def get(self, key: str) -> Any:
        if not self._available:
            return None

        var = self.coll.find_one({'key': key})
        if var:
            return var['value']
        else:
            return None

    def set(self, key: str, value: Any) -> None:
        ...
