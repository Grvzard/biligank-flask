import time

from .utils import ts2date, ts2date_2, ts2clock


def register_jinja_filters(app):
    app.jinja_env.filters['strftime'] = ts2date
    app.jinja_env.filters['strftime_2'] = ts2date_2
    app.jinja_env.filters['ts2clock'] = ts2clock
