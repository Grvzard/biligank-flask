
from flask import Blueprint, current_app, render_template, request

from ..logger import MultiLogger
from ..utils import get_time
from . import live

bp = Blueprint(
    name='general',
    import_name=__name__,
)


bp.add_url_rule(
    rule='/',
    view_func=live.index,
)


feedback_logger = MultiLogger(**current_app.config['FEEDBACK_LOGGER'])


@bp.route('/feedback', methods=['POST'])
def feedback():
    content_type = request.headers.get("content_type")
    assert content_type is not None
    if content_type == 'application/json':
        assert request.json is not None
        text = request.json.get('text')
    elif content_type.startswith('application/x-www-form-urlencoded'):    
        text = request.form['text']
    else:
        raise Exception('unknown content type')

    data = {
        'time': get_time(),
        'text': text,
        'ip': request.headers.get('x-real-ip'),
    }
    feedback_logger.log(data)
    return 'ok'


@bp.route('/about')
def about():
    return render_template('about.html', status={})


@bp.route('/metrics')
def metrics():
    kvdb = current_app.extensions['kvdb']
    return kvdb.get('status') or {}
