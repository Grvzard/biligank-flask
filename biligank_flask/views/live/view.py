
from flask import Blueprint, current_app, render_template, request
from flask.views import View

from biligank_flask.logger import SearchLogger
from biligank_flask.utils import Timer

from .ablive_searcher import AbliveSearcher
from .livedm_searcher import LivedmSearcher
from .liveroom_searcher import LiveroomSearcher

__all__ = 'bp',


class AbliveView(View):
    init_every_request = False
    methods = ["GET"]

    def __init__(self, road, searcher, liveroom_searcher):
        self.road = road
        self.template = f'live/{road}.tmpl.html'
        if road == 'livedm':
            self.template = 'live/ablive_dm.tmpl.html'
        self.searcher = searcher
        self.liveroom = liveroom_searcher

    def dispatch_request(self):
        road = self.road
        uid = request.args.get('uid', type=int)
        offset = request.args.get('offset')
        not_render = bool(request.args.get('not_render'))
        first_time = True if offset == '0' else False

        if not isinstance(uid, int):
            raise Exception('invalid uid')

        timer = Timer()
        with timer:
            data, next_offset, has_more, liverids = self.searcher.more(uid, offset)
            rooms_dict = self.liveroom.get_livers_info(liverids)

        search_logger.log(
            uid = uid,
            road = road,
            offset = offset,
            loadtime = timer.result,
            ip = request.headers.get('x-real-ip'),
            not_render = not_render,
        )

        resp = {
            "road": road,
            "uid": uid,
            "next_offset": next_offset,
            "first_time": first_time,
            "data": data,
            "rooms_dict": rooms_dict,
            "has_more": has_more,
        }

        if not_render:
            return resp

        return render_template(
            self.template,
            **resp,
        )


MONGO_CONFIG = current_app.config['ABLIVE']['MONGO_CONFIG']
ROADS = current_app.config['ABLIVE']['ROADS']
LIMITS = current_app.config['ABLIVE']['LIMITS']

liveroom_searcher = LiveroomSearcher(MONGO_CONFIG)
search_logger = SearchLogger(
    **current_app.config['SEARCH_LOGGER']
)


bp = Blueprint(
    name='live',
    import_name=__name__,
    url_prefix='/live',
)


for road in ROADS:
    if road == 'livedm':
        bp.add_url_rule(
            rule="/livedm",
            view_func=AbliveView.as_view(
                name='livedm',
                road='livedm',
                searcher=LivedmSearcher(
                    MONGO_CONFIG,
                    limits=LIMITS['livedm'],
                ),
                liveroom_searcher=liveroom_searcher,
            ),
        )
    else:
        bp.add_url_rule(
            rule=f"/{road}",
            view_func=AbliveView.as_view(
                name=f'{road}',
                road=f'{road}',
                searcher=AbliveSearcher(
                    road=f'{road}',
                    limits=LIMITS[f'{road}'],
                ),
                liveroom_searcher=liveroom_searcher,
            ),
        )


@bp.route('/')
def index():
    return render_template(
        'live/index.html',
        notice=[],
    )


@bp.route('/data')
def data():
    raise Exception('deprecated route')
