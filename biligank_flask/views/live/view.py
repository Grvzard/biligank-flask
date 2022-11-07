import time

from flask import render_template, request
from flask.views import View

from biligank_flask.utils import Timer

__all__ = 'AbliveView',


class AbliveView(View):
    init_every_request = False
    methods = ["GET"]

    def __init__(self, road, searcher, liveroom_searcher, search_logger):
        self.road = road
        self.template = f'live/{road}.tmpl.html'
        if road == 'livedm':
            self.template = 'live/ablive_dm.tmpl.html'
        self.searcher = searcher
        self.liveroom = liveroom_searcher
        self.search_logger = search_logger

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

        self.search_logger.log({
            'uid': uid,
            'road': road,
            'offset': offset,
            'loadtime': timer.result,
            'ip': request.headers.get('x-real-ip'),
            'not_render': not_render,
            'ts': int(time.time()),
        })

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


