from flaskr.db import MessageInfo, db
from sqlalchemy.sql import func
from collections import defaultdict, Counter
from functools import reduce


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
