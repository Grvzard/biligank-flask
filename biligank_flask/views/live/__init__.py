
from flask import Blueprint, current_app, render_template

from ...kvdb import kvdb
from ...logger import MultiLogger
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

ROADS = current_app.config['ABLIVE']['ROADS']
LIMITS = current_app.config['ABLIVE']['LIMITS']

liveroom_searcher = LiveroomSearcher()
search_logger = MultiLogger(
    **current_app.config['SEARCH_LOGGER']
)

for road in ROADS:
    if road == 'livedm':
        searcher = LivedmSearcher(
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
