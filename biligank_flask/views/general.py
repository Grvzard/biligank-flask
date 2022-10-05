
from flask import Blueprint, current_app, render_template, request

from biligank_flask.kvdb import KvDb
from biligank_flask.logger import FeedbackLogger
from biligank_flask.utils import get_time

from . import live

bp = Blueprint(
    name='general',
    import_name=__name__,
)


bp.add_url_rule(
    rule='/',
    view_func=live.view.index,
)


feedback_logger = FeedbackLogger(**current_app.config['FEEDBACK_LOGGER'])
kvdb = KvDb(**current_app.config['KV_DB'])


@bp.route('/feedback', methods=['POST'])
def feedback():
    text = request.form['text']
    data = {
        'time': get_time(),
        'text': text,
        'ip': request.headers.get('x-real-ip'),
    }
    feedback_logger.log(data)
    return 'ok'


@bp.route('/about')
def about():
    status = kvdb.get('status')
    return render_template('about.html', status=status)
