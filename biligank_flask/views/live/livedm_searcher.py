from typing import Any, Optional

from flask import current_app


class LivedmSearcher:
    def __init__(self, limits: int) -> None:
        self.limits = limits
        self.update_colls(current_app.extensions['mongo_client']['livedm'])

    def update_colls(self, db) -> None:
        colls = db.list_collection_names()
        colls.sort(reverse=False)
        self.colls = colls
        self.last_coll = colls[-1]

    def more(self, uid: int, offset: str) -> tuple[Optional[list[Any]], str, bool, set[Optional[int]]]:  # noqa
        db = current_app.extensions['mongo_client']['livedm']

        try:
            if offset == '0':
                offset = self.last_coll
                table_idx = self.colls.index(offset) + 1
            else:
                table_idx = self.colls.index(offset)
        except Exception as e:
            raise e

        data = []
        liverids = set()
        while table_idx > 0:
            table_idx -= 1
            table = self.colls[table_idx]

            _data, _liverids = self.daily_docs(db, table, uid)
            data.extend(_data)
            liverids |= _liverids

            if len(data) >= self.limits:
                break

        next_offset = table
        has_more = False if table_idx == 0 else True

        return data, next_offset, has_more, liverids

    def daily_docs(self, db, date: str, uid: int) -> tuple[list, set]:
        docs = db[date].find({
                'uid': uid,
            }, {
                '_id': 0,
            },
        )
        date_dm_cards = []
        _liverids = set()
        for doc in docs:
            doc['dm'].sort(reverse=False)

            dm_card = {
                'date': date,
                'liverid': doc['liverid'],
                'danmakus': doc['dm'],
            }
            _liverids.add(doc['liverid'])
            date_dm_cards.append(dm_card)

        return date_dm_cards, _liverids

    def get_doc(self, uid: int, liverid: int, date: str) -> Optional[dict[str, Any]]:
        part = date[:7]
        doc = self.mongo_client[f'livedm_{part}'][date].find_one({
                'uid': uid,
                'liverid': int(liverid),
            }, {
                '_id': 0,
            },
        )
        if doc:
            doc['dm'].sort(reverse=False)

        return doc
