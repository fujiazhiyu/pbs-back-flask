from flaskr.db import MessageInfo


def recommendRoads(params):
    results = MessageInfo.query.filter(MessageInfo.id.in_(tuple(params["selected_points"]))).all()
    res = {
        "status": 'success',
        "count": len(results),
        "data": [r.format('id', 'keywords', 'lng', 'lat', method='PICK') for r in results]
    }
    return res
