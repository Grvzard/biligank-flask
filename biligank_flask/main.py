import time

from flask import Flask, render_template, request

from biligank_flask.logger import JsonLogger
from biligank_flask.utils import get_time


app = Flask(__name__)

app.config.from_prefixed_env()

if app.config['DEBUG']:
    app.config.from_object('app_configs.DevConfig')
else:
    app.config.from_object('app_configs.ProdConfig')

from .mongodb import mongodb
from .kvdb import kvdb
mongodb.init_app(app)
kvdb.init_app(app)

with app.app_context():
    from .views import general, live
    app.register_blueprint(general.bp)
    app.register_blueprint(live.bp)

from .sqldb import db
db.init_app(app)

from .jinja_filters import register_jinja_filters
register_jinja_filters(app)


error_logger = JsonLogger('logs/error')
ERROR_TEXT = app.config['ERROR_TEXT']

@app.errorhandler(Exception)
def default_error(e):
    data = {
        "time": get_time(),
        "path": request.full_path,
        "info": str(e),
        "ip": request.headers.get('x-real-ip'),
    }
    error_logger.log(data)
    return ERROR_TEXT


@app.errorhandler(404)
def page_notfound(error):
    return render_template('404.html'), 404
