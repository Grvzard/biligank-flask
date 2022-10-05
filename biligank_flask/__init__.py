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


with app.app_context():
    from .views import general, live
    app.register_blueprint(general.bp)
    app.register_blueprint(live.bp)

from .sqldb import db

db.init_app(app)


@app.template_filter('strftime')
def _jinja2_filter_strftime(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)

@app.template_filter('strftime_2')
def _jinja2_filter_strftime_2(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%m-%d %H:%M", struct_time)

@app.template_filter('ts2clock')
def _jinja2_filter_ts2clock(time_stamp):
    struct_time = time.localtime(time_stamp)
    return time.strftime("%H:%M:%S", struct_time)


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
