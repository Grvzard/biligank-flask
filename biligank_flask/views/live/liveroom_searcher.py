from typing import Sequence, Union

import pymongo

from ...mongodb import mongodb


class LiveroomSearcher:
    def __init__(self, mongo_config: str):
        # self.mongo_client: pymongo.MongoClient = pymongo.MongoClient(mongo_config)
        self.mongo_client = mongodb.client
        self.db = self.mongo_client['bili_liveroom']

    def get_livers_info(self, liverids: Union[Sequence[int], set[int]]):
        liverids = list(liverids)
        rooms_dict = {}
        for coll in ('all', 'rooms_state'):
            rs = self.db[coll].find({
                'uid': {
                    '$in': liverids},
                }, {
                'uid': 1, 'uname': 1, 'area_name': 1, '_id': 0,
                })
            for room_info in rs:
                liverid = int(room_info['uid'])
                rooms_dict[liverid] = room_info

        return rooms_dict

    def get_liver_info(self, liverid: Union[int, str]):
        liverid = int(liverid)
        for coll in ('all', 'rooms_state'):
            room_info = self.db[coll].find_one({
                'uid': liverid
                }, {
                'uname': 1, 'area_name': 1, '_id': 0
                })
            if room_info:
                break
        else:
            room_info = {
                'uname': 'bug',
                'area_name': 'bug',
            }

        return room_info
