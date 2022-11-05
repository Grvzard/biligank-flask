from typing import Any, Optional

import pymongo


class MongoDB:
    client = None

    def init_app(self, app) -> None:
        config = app.config['ABLIVE']['MONGO_CONFIG']
        self.client: pymongo.MongoClient = pymongo.MongoClient(config)


mongodb = MongoDB()
