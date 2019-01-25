from flaskr.db import MessageInfo, Cluster, db
from sqlalchemy.sql import func
from functools import reduce
from collections import Counter


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
