# coding:utf-8
from flaskr.db import MessageInfo, Cluster, db
from sqlalchemy.sql import func
import sys
import math
import time
from collections import defaultdict, Counter
from functools import reduce


# def pickDataset(args):
#     results = Testdata.query.filter_by(**args).all()
#     res = {
#             "status": "1",
#             "count": len(results),
#             "data": [r.format() for r in results]
#           }
#     return res

def pickData(args, api):
    if 'date' in args:
        dt = getDateRange(args['date'][0])
        if dt is None:
            return {
                "status": 0,
                "info": "date parameter error..."
            }

    if api == 'messages':
        return pickPoints(dt)

    if api == 'themes':
        return pickThemes(dt)

    if api == 'keywords':
        return pickKeywords(dt, args['themes'][0], args['time'][0])


def pickPoints(dt):
    # results = MessageInfo.query.filter(MessageInfo.recitime > dt[0], MessageInfo.recitime < dt[1]).limit(10000).all()
    results = MessageInfo.query.filter(
        MessageInfo.conntime > dt[0], MessageInfo.conntime < dt[1]).all()
    res = {
        "status": '1',
        "count": len(results),
        "data": [r.format('phone', method='UNPICK') for r in results]
    }
    return res


def pickThemes(dt):
    tempT = db.session().query(MessageInfo.theme, func.FROM_UNIXTIME(MessageInfo.conntime / 1000, '%k').label("hour")
                               ).filter(MessageInfo.conntime > dt[0], MessageInfo.conntime < dt[1]).subquery(name='T')
    results = db.session().query(tempT.c.theme, tempT.c.hour, func.count(
        tempT.c.theme).label("theme_count")).group_by(tempT.c.theme, tempT.c.hour).all()
    res = {
        "status": 1,
        "count": 1,
        "data": countThemes(results)
    }
    return res


def pickKeywords(dt, themes, time):
    selectedThemes = tuple(list(map(int, themes.split(','))))
    startTime, endTime = list(map(int, time.split(',')))
    results = db.session().query(MessageInfo.keywords, func.COUNT(MessageInfo.keywords).label("keywords_count")).filter(MessageInfo.conntime > dt[0], MessageInfo.conntime < dt[1], MessageInfo.theme.in_(selectedThemes), (func.FROM_UNIXTIME(
        MessageInfo.conntime / 1000, '%k') * 60 + func.FROM_UNIXTIME(MessageInfo.conntime / 1000, '%i')) > startTime, (func.FROM_UNIXTIME(MessageInfo.conntime / 1000, '%k') * 60 + func.FROM_UNIXTIME(MessageInfo.conntime / 1000, '%i')) < endTime).group_by(MessageInfo.keywords).all()
    counts = reduce(lambda x, y: x + y, [Counter({key: keywords[1]})
                                         for keywords in results if keywords[0] for key in keywords[0].split(';')])
    result = dict(counts)
    themeNum = {'代开发票': '01', '银行积分': '02', '信用卡提额': '03', '账户解冻': '04', '贷款': '05', '线上兼职': '06', '股票金融': '07', '诈取设备密码': '08', '色情服务': '09', '套现提现': '10', '银行提醒': '11', '冒充移动诈骗': '12', '办证刻章': '13', '房地产': '14', '赌博': '15', '广告': '16', '胡言乱语': '17', '非法广告': '18'}
    keywordsNum = {}
    for key in result.keys():
        if key not in keywordsNum:
            keywords_theme = db.session().query(Cluster.theme).filter(func.LOCATE(key, Cluster.keywords) != 0).distinct().all()
            keywordsNum.update({key: themeNum[keywords_theme[0][0]]})

    print(keywordsNum)
    res = {
        "status": "success",
        "records": [{"text": r, "weight": result[r], "html": {"class": "theme-color-" + keywordsNum[r], "draggable": "true"}} for r in result.keys()]
    }
    return res


def pickContacts(args):
    results = db.session().query(Cluster.contacts, Cluster.theme, func.SUM(Cluster.count).label("contacts_count")
                                 ).filter(Cluster.contacts.isnot(None)).group_by(Cluster.theme, Cluster.contacts).limit(10).all()
    res = {
        "code": 0,
        "msg": "",
        "count": len(results),
        "data": [{"id": i, "contacts": results[i][0], "theme": results[i][1], "count": int(results[i][2])} for i in range(len(results))]
    }
    return res


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


def countThemes(results):
    # 5大类分别包含哪些子类
    themeIndexes = [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9]]
    # 10子类分别包含哪些初始类别
    subThemeIndexes = [[5, 10], [7], [6], [14], [16], [
        1, 13], [9, 15, 18], [2, 3, 4, 11], [8, 12], [17]]
    # 三元turple转嵌套dict [(x,y,z), ..] => {x:{y: z, y2: z2, ..}, ..}
    tuple3dict = defaultdict(dict)
    for x, y, z in results:
        tuple3dict[x][y] = z

    subdata = {}
    for subtheme in subThemeIndexes:
        subresult = []
        for s in subtheme:
            subresult.append(Counter(tuple3dict[s]))
            # Counter({'a': 1}) + Counter({'a': 3}) 可以合并计数: Counter({'a': 4})
        subdata[subThemeIndexes.index(subtheme)] = dict(
            reduce(lambda x, y: x + y, subresult))

    data = {}
    for ti in themeIndexes:
        data[themeIndexes.index(ti)] = []
        for sti in ti:
            hours = []
            for l in range(23):
                hours.append(subdata[sti].pop(str(l), 0))
            data[themeIndexes.index(ti)].append(
                {'subTheme': sti, 'hours': hours})

    return data
