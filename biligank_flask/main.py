
from flask import Flask, render_template, request, current_app

from .logger import JsonLogger
from .utils import get_time

app = Flask(__name__)

app.config.from_prefixed_env()

if app.config['DEBUG']:
    app.config.from_object('app_configs.DevConfig')
else:
    app.config.from_object('app_configs.ProdConfig')

from flask_sqlalchemy import SQLAlchemy
from .mongodb import MongoDB
from .kvdb import KvDb
sqldb = SQLAlchemy(app)
mongodb = MongoDB(app)
kvdb = KvDb(app)

with app.app_context():
    from .views import general, live
    app.register_blueprint(general.bp)
    app.register_blueprint(live.bp)

from .jinja_filters import register_jinja_filters
register_jinja_filters(app)

error_logger = JsonLogger('error.json')


@app.errorhandler(Exception)
def default_error(e):
    data = {
        "time": get_time(),
        "path": request.full_path,
        "info": str(e),
        "ip": request.headers.get('x-real-ip'),
    }
    error_logger.log(data)
    return current_app.config['ERROR_TEXT']


@app.errorhandler(404)
def page_notfound(error):
    return render_template('404.html'), 404
