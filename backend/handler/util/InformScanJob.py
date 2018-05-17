# -*- coding: utf-8 -*-
#
import datetime
import sys
import traceback
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from backend.common.consts import Const
from backend.handler.util.DateUtil import DateUtil
from backend.handler.util.Util import Util

class InformScanJob(object):
    scheduler = BackgroundScheduler()

    def __init__(self, settings):
        self.settings = settings
        self._inform_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "inform_info")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._user_group_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_group_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")
        self._scheduler_scan_time = self.settings['kinder_mongo_pool'].get_collection('kinder', "scheduler_scan_time")
        self._scanned_user_notification_list = self.settings['kinder_mongo_pool'].get_collection('kinder', "scanned_user_notification_list")
        self._scanned_user_inform_list = self.settings['kinder_mongo_pool'].get_collection('kinder', "scanned_user_inform_list")

    def startScan(self):
        self.scheduler.start()
        self.scheduler.add_job(self.scanJob, 'interval', minutes=1, max_instances=6)

    def matchWeekDay(self, weekDay, periodDate):
        weekDayid = 'DUTY_PERIOD_WEEK_' + str(weekDay)
        return (weekDayid in periodDate)

    def matchMonthDay(self, monthDay, periodDate):
        monthDayid = 'DUTY_PERIOD_DATE_' + str(monthDay)
        return (monthDayid in periodDate)

    def shouldPickDuty(self, duty, startofday):
        if duty['timeType'] == Const.DUTY_TIME_TYPE_ROUTINE:
            return True
        elif duty['timeType'] == Const.DUTY_TIME_TYPE_PERIODICAL:
            date = datetime.datetime.fromtimestamp(startofday)
            if duty['periodType'] == Const.DUTY_PERIOD_TYPE_WEEK:
                # 计算startofday 是星期几
                return self.matchWeekDay(date.weekday(), duty['periodDate'])
            elif duty['periodType'] == Const.DUTY_PERIOD_TYPE_MONTH:
                # 计算startofday 是一个月的第几天
                return self.matchMonthDay(date.day, duty['periodDate'])
        elif duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
            if duty['starttime'] <= startofday and duty['endtime'] > startofday:
                return True
        return False

    def getUserGroupDuty(self, userId):
        duties = []
        userGroups = self._user_group_info_coll.find()
        if userGroups:
            for group in userGroups:
                if userId in group['members']:
                    duties = duties + group['duty']
        return duties

    def scanJob(self):
        allUsers = list(Util.getAllUser(self._user_info_coll))
        self.scanUserNotification(allUsers)
        self.scanUserInform(allUsers)

    def scanUserNotification(self, allUsers):
        scanInfo = self._scheduler_scan_time.find_one({'_id': 'user_notification_scan'})
        lastScanTime = 0
        if scanInfo != None:
            lastScanTime = scanInfo['lastScanTime']
        else:
            scanInfo = {'_id': 'user_notification_scan'}
        result = []
        allDuties = list(self._duty_info_coll.find())
        allExecData = list(self._task_exec_data_coll.find())
        for user in allUsers:
            queryTime = DateUtil.get_current_time()
            startofday = DateUtil.get_startof_today()
            userDuties = user['duty']
            groupDuties = self.getUserGroupDuty(user['_id'])
            if len(groupDuties) > 0:
                userDuties = userDuties + groupDuties
            allUserDuties = Util.getDutyByIds(allDuties, userDuties)

            for index, duty in enumerate(allUserDuties):
                if not self.shouldPickDuty(duty, startofday) or not duty['notify_user']:
                    # 如果此职责不需要显示在查询的date的职责列表上的话，直接跳过
                    continue
                dutyId = duty['_id']
                if 'notify_user_setting_list' in duty and len(duty['notify_user_setting_list']) > 0:
                    query = {'userid': user['_id'], 'taskid': dutyId, 'startofday': startofday}
                    data = Util.getTaskExecData(user['_id'], dutyId, startofday, allExecData)
                    item = {}
                    if not data:
                        dutyRealStarttime = duty['startime'] if (
                        duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC) else startofday + duty['starttime']
                        dutyRealEndtime = duty['endtime'] if (
                        duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC) else startofday + duty['endtime']
                        for notify in duty['notify_user_setting_list']:
                            match = False
                            if notify['timeType'] == Const.NOTIFY_TIME_TYPE_BEFORE \
                                    and queryTime >= (dutyRealStarttime - notify['timeLength'] * 60 > lastScanTime):
                                item['informSendTime'] = (dutyRealStarttime - notify['timeLength'] * 60)
                                match = True
                            elif notify['timeType'] == Const.NOTIFY_TIME_TYPE_AFTER \
                                    and queryTime >= (dutyRealEndtime + notify['timeLength'] * 60 > lastScanTime):
                                item['informSendTime'] = (dutyRealEndtime + notify['timeLength'] * 60)
                                match = True
                            elif notify['timeType'] == Const.NOTIFY_TIME_TYPE_SPECIFIC \
                                    and (queryTime >= notify['timePoint'] > lastScanTime):
                                item['informSendTime'] = notify['timePoint']
                                match = True

                            if match:
                                item['_id'] =  '{:s}_{:s}_{:d}_{:s}'.format(user['_id'], dutyId, int(startofday), notify['timeType'])
                                item['userid'] = user['_id']
                                item['taskid'] = dutyId
                                item['taskname'] = duty['name']
                                item['taskDescr'] = duty['descr']
                                item['realstarttime'] = dutyRealStarttime
                                item['realendtime'] = dutyRealEndtime
                                item['dutyTimeType'] = duty['timeType']
                                item['notifyTimeType'] = notify['timeType']
                                item['notifyType'] = notify['notifyType']
                                item['notifyPriority'] = notify['notifyPriority']
                                item['createTime'] = queryTime
                                item['isNew'] = True
                                result.append(item)
        if len(result) > 0:
            self._scanned_user_notification_list.insert(result)
        scanInfo['lastScanTime'] = queryTime
        self._scheduler_scan_time.save(scanInfo)

    def scanUserInform(self, allUsers):
        scanInfo = self._scheduler_scan_time.find_one({'_id': 'user_inform_scan'})
        lastScanTime = 0
        if scanInfo != None:
            lastScanTime = scanInfo['lastScanTime']
        else:
            scanInfo = {'_id': 'user_inform_scan'}
        queryTime = DateUtil.get_current_time()
        allInform = list(self._inform_info_coll.find({'sendTime': {'$lte': queryTime, '$gt': lastScanTime}}))
        result = []
        try:
            for user in allUsers:
                for inform in allInform:
                    if user['_id'] in inform['informUserList']:
                        item = {}
                        item['_id'] = '{:s}_{:s}_{:d}'.format(user['_id'], inform['_id'], inform['sendTime'])
                        item['notifyType'] = inform['notifyType']
                        item['notifyPriority'] = inform['notifyPriority']
                        item['name'] = inform['name']
                        item['seq'] = inform['seq']
                        item['sendTime'] = inform['sendTime']
                        item['descr'] = inform['descr']
                        item['userid'] = user['_id']
                        item['sender'] = inform['sender']
                        item['createTime'] = queryTime
                        item['isNew'] = True
                        result.append(item)
            if len(result) > 0:
                self._scanned_user_inform_list.insert(result)
            scanInfo['lastScanTime'] = queryTime
            self._scheduler_scan_time.save(scanInfo)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # traceback.print_exception(exc_type, exc_value, exc_traceback)
            # traceback.print_exc()
            # logging.getLogger().critical(traceback.format_exc())
