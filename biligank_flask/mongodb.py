
from flask import Flask
import pymongo


class MongoDB:
    client = None

    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        config = app.config['ABLIVE']['MONGO_CONFIG']
        self.client = pymongo.MongoClient(config)

        app.extensions['mongo_client'] = self.client
