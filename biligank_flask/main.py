
from flask import Flask, render_template, current_app


app = Flask(__name__)


if app.debug:
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

from .logging import configure_logging
configure_logging(app)


@app.errorhandler(Exception)
def default_error(e):
    current_app.logger.error(str(e))
    return current_app.config['ERROR_TEXT']


@app.errorhandler(404)
def page_notfound(error):
    return render_template('404.html'), 404
