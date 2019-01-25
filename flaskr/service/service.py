# coding:utf-8
from .pickthemes import pickThemes
from .pickmessages import pickMessages
from .pickkeywords import pickKeywords
from .pickcontacts import pickContacts
from .recommendroads import recommendRoads
import time


def pickData(args, api):
    if api == 'contacts':
        return pickContacts(args)

    if api == 'recommend':
        return recommendRoads(args)

    if 'date' in args:
        dt = getDateRange(args['date'][0])
        if dt is None:
            return {
                "status": 0,
                "info": "date parameter error..."
            }

    if api == 'messages':
        return pickMessages(dt)

    if api == 'themes':
        return pickThemes(dt)

    if api == 'keywords':
        return pickKeywords(dt, args['themes'][0], args['time'][0])


def getDateRange(dt):
    """ 获取时间戳范围
    参数
    --------------
    dt: str
        url请求中传递过来的date参数

    返回值
    --------------
    turple
        返回一对 (起始时间戳,终止时间戳)
    """
    if dt == 'weekend':
        startDT = "2017-03-25 00:00:00"
        endDT = "2017-03-27 00:00:00"
    elif dt == 'weekday':
        startDT = "2017-03-20 00:00:00"
        endDT = "2017-03-25 00:00:00"
    else:
        return None

    startTimeArray = time.strptime(startDT, "%Y-%m-%d %H:%M:%S")
    endTimeArray = time.strptime(endDT, "%Y-%m-%d %H:%M:%S")
    return (time.mktime(startTimeArray) * 1000, time.mktime(endTimeArray) * 1000)
