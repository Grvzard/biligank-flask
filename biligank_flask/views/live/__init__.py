
from flask import Blueprint, current_app, render_template

from biligank_flask.logger import MultiLogger
from biligank_flask.kvdb import kvdb

from .ablive_searcher import AbliveSearcher
from .livedm_searcher import LivedmSearcher
from .liveroom_searcher import LiveroomSearcher
from .view import AbliveView

__all__ = 'bp',


bp = Blueprint(
    name='live',
    import_name=__name__,
    url_prefix='/live',
)


MONGO_CONFIG = current_app.config['ABLIVE']['MONGO_CONFIG']
ROADS = current_app.config['ABLIVE']['ROADS']
LIMITS = current_app.config['ABLIVE']['LIMITS']

liveroom_searcher = LiveroomSearcher(MONGO_CONFIG)
search_logger = MultiLogger(
    **current_app.config['SEARCH_LOGGER']
)

for road in ROADS:
    if road == 'livedm':
        searcher = LivedmSearcher(
            MONGO_CONFIG,
            limits=LIMITS['livedm'],
        )
    else:
        searcher = AbliveSearcher(
            road=f'{road}',
            limits=LIMITS[f'{road}'],
        )

    bp.add_url_rule(
        rule=f"/{road}",
        view_func=AbliveView.as_view(
            name=f'{road}',
            road=f'{road}',
            searcher=searcher,
            liveroom_searcher=liveroom_searcher,
            search_logger=search_logger,
        ),
    )


@bp.route('/')
def index():
    notice = kvdb.get('notice')
    return render_template(
        'live/index.html',
        notice=notice,
        # notice=[],
    )


@bp.route('/data')
def data():
    raise Exception('deprecated route')
