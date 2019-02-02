from flaskr.db import MessageInfo
import asyncio
from collections import Counter
from .asynroadinfo import generateURLS, crawlInfo


def recommendRoads(params):
    results = []
    for pt in splitPointTuple(params["selected_points"], 10000):
        resultpiece = MessageInfo.query.filter(MessageInfo.id.in_(pt)).all()
        results.extend([r.format('id', 'keywords', 'lng', 'lat', method='PICK') for r in resultpiece])

    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    roadsinfo = crawlInfo(generateURLS(results))
    impactedroads = integrateRoads(roadsinfo["data"], results, params["keywords_weights"])
    res = {
        "status": 'success',
        "pointcount": len(results),
        "roadcount": len(impactedroads.keys()),
        "data": impactedroads
    }
    return res


def splitPointTuple(points_list, length):
    while len(points_list) != 0:
        yield tuple(points_list[:length])
        points_list[:length] = []


def integrateRoads(roadsInfo, results, keywords_weights):
    impactedRoads = {}
    indexes = roadsInfo.keys()
    for bundleIdx in indexes:   # indexes本身就是顺序的数字组成的: {"0": , "1": , ...}
        # roadsInfo is a dict, pick a bundle in it
        for batchIdx in range(len(roadsInfo[bundleIdx])):
            batch = roadsInfo[bundleIdx][batchIdx]
            if batch["status"] == 200 and batch["body"]["status"] == "1":
                for pointIdx in range(len(batch["body"]["regeocodes"])):
                    point = batch["body"]["regeocodes"][pointIdx]
                    selected_pointsIndex = int(bundleIdx) * 400 + batchIdx * 20 + pointIdx
                    for road in point["roads"]:
                        kwsStr = results[selected_pointsIndex]["keywords"]
                        keywords = kwsStr.split(';') if kwsStr else ""
                        pointContr, KWContrs = keywordContributions(keywords, keywords_weights, float(road["distance"]))
                        road["keywords"] = KWContrs
                        road["contribution"] = pointContr
                        road["pointId"] = results[selected_pointsIndex]["id"]
                        if road["id"] in impactedRoads:     # 如果有此键
                            merge2road(impactedRoads[road["id"]], road)
                        else:
                            impactedRoads[road["id"]] = {"locations": [road["location"]]}
                            impactedRoads[road["id"]]["pointIds"] = [road["pointId"]]
                            impactedRoads[road["id"]]["weight"] = road["contribution"]
                            impactedRoads[road["id"]]["keywords"] = Counter(road["keywords"])

    return impactedRoads


def merge2road(totalroad, newroad):
    totalroad["pointIds"].append(newroad["pointId"])
    totalroad["weight"] = totalroad["weight"] + newroad["contribution"]
    totalroad["locations"].append(newroad["location"])
    totalroad["keywords"].update(newroad["keywords"])   # Counter({"kw1": contrs})


def keywordContributions(keywords, keywords_weights, distance):
    KWContrs = {}
    totalContr = 0
    for kw in keywords:
        if kw in keywords_weights:
            sigKW = (keywords_weights[kw] - 50) * 2 + 50 * 1.5
        else:
            sigKW = 50
        disImpact = 1000 / distance
        KWContrs[kw] = sigKW * disImpact
        totalContr += sigKW * disImpact

    return totalContr, KWContrs
