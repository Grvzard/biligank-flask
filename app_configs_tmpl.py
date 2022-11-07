
class Config:
    ERROR_TEXT = "出错了。"
    ABLIVE = {
        "MONGO_CONFIG": "mongodb://localhost:27017/",
        "ROADS": ["ablive_dm", "ablive_en", "ablive_gf", "ablive_sc", "tp", "livedm"],
        "LIMITS": {
            'ablive_dm': 2,
            'ablive_en': 5,
            'ablive_gf': 2,
            'ablive_sc': 1,
            'tp': 5,
            'livedm': 9,
        },
    }
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://localhost:3306/tp"
    SQLALCHEMY_BINDS = {
        "ablive_dm": "mysql+pymysql://localhost:3306/ablive_dm",
        "ablive_en": "mysql+pymysql://localhost:3306/ablive_en",
        "ablive_gf": "mysql+pymysql://localhost:3306/ablive_gf",
        "ablive_sc": "mysql+pymysql://localhost:3306/ablive_sc",
        "tp": "mysql+pymysql://localhost:3306/tp",
    }
    SEARCH_LOGGER = {
        "json": "search_log.json",
    }
    FEEDBACK_LOGGER = {
        "json": "feedback.json",
    }
    KV_DB = {
        "config": "",
    }
