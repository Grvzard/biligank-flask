from typing import Any, Optional

import pymongo


class KvDb:
    def init_app(self, app) -> None:
        config = app.config['ABLIVE']['MONGO_CONFIG']
        self.client: pymongo.MongoClient = pymongo.MongoClient(config)
        self.coll = self.client['biligank_web']['var']

    def get(self, key: str) -> Optional[Any]:
        var = self.coll.find_one({'key': key})
        if var:
            return var['value']
        else:
            return None

    def set(self, key: str, value: Any) -> None:
        ...

kvdb = KvDb()
