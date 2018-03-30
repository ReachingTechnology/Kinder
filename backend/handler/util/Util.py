# -*- coding: utf-8 -*-
#
import hashlib

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

    @classmethod
    def getDutyByIds(cls, allDuty, dutyIds):
        result = []
        for duty in allDuty:
            if duty['_id'] in dutyIds:
                result.append(duty)
        return result

    @classmethod
    def getTaskExecData(cls, userid, taskid, startofday, allData):
        for data in allData:
            if data['userid'] == userid and data['taskid'] == taskid and data['startofday'] == startofday:
                return data
        return None

    @staticmethod
    def get_md5_str(value):
        return hashlib.md5(value).hexdigest()

    @classmethod
    def get_str_md5(cls, input_str):
        md5obj = hashlib.md5(input_str)
        hash_value = md5obj.hexdigest()
        return hash_value