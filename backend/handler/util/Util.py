# -*- coding: utf-8 -*-
#

class Util(object):
    @classmethod
    def getAllUser(cls, coll):
        query = {"_id": {"$ne": 'admin'}}
        results = coll.find(query)

        return results