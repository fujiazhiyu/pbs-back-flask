from flaskr.db import MessageInfo
# from sqlalchemy.sql import func


def pickMessages(dt):
    # results = MessageInfo.query.filter(MessageInfo.recitime > dt[0], MessageInfo.recitime < dt[1]).limit(10000).all()
    results = MessageInfo.query.filter(
        MessageInfo.conntime > dt[0], MessageInfo.conntime < dt[1]).all()
    res = {
        "status": '1',
        "count": len(results),
        "data": [r.format('phone', method='UNPICK') for r in results]
    }
    return res
