from flaskr.db import Cluster, db
from sqlalchemy.sql import func


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
