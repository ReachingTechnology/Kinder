# -*- coding: utf-8 -*-
#

class Util(object):
    @classmethod
    def getAllUser(cls, coll):
        query = {"_id": {"$ne": 'admin'}}
        results = coll.find(query)

        return results

    @classmethod
    def getAllUnderlingWithSelf(cls, self, coll):

        # query = {"_id": {"$nin": ['admin', self]}, "leader": self}
        query = {"_id": {"$ne": 'admin'}}
        allUsers = list(coll.find(query))
        users = []
        userLen = len(allUsers)
        if allUsers != None and userLen > 0:
            users = cls.getAllUnderlingFromList(self, allUsers)
        else:
            return []

        me = coll.find_one({'_id': self})
        result = []
        result.append(me)
        result.extend(users)
        return result

    @classmethod
    def getAllUnderling(cls, self, coll):

        # query = {"_id": {"$nin": ['admin', self]}, "leader": self}
        query = {"_id": {"$ne": 'admin'}}
        allUsers = list(coll.find(query))
        users = []
        userLen = len(allUsers)
        if allUsers != None and userLen > 0:
            users = cls.getAllUnderlingFromList(self, allUsers)
        else:
            return []

        result = []
        result.extend(users)
        return result

    @classmethod
    def getAllUnderlingFromList(cls, self, userList):
        users = []
        for user in userList:
            if user['leader'] == self and user['_id'] != self:
                users.append(user)
        userLen = len(users)
        if userLen > 0:
            for i in range(userLen):
                users.extend(cls.getAllUnderlingFromList(users[i]['_id'], userList))
        else:
            return []
        return users