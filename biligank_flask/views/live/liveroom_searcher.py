from collections.abc import Sequence
from typing import Union


def get_livers_info(db, liverids: Sequence[int]):
    rooms_dict = {}
    for coll in ('all', 'rooms_state'):
        rs = db[coll].find({
                'uid': {'$in': list(liverids)},
            }, {
                'uid': 1, 'uname': 1, 'area_name': 1, '_id': 0,
            },
        )
        for room_info in rs:
            liverid = int(room_info['uid'])
            rooms_dict[liverid] = room_info

    return rooms_dict


def get_liver_info(db, liverid: Union[int, str]):
    for coll in ('all', 'rooms_state'):
        room_info = db[coll].find_one({
                'uid': int(liverid)
            }, {
                'uname': 1, 'area_name': 1, '_id': 0
            },
        )
        if room_info:
            break
    else:
        room_info = {
            'uname': 'bug',
            'area_name': 'bug',
        }

    return room_info
