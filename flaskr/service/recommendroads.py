from flaskr.db import MessageInfo
from sklearn.cluster import DBSCAN
import pandas as pd, numpy as np
from math import *
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

    # recicoords = [[r['lng'], r['lat']] for r in results]
    roadsinfo = crawlInfo(generateURLS(results))
    impactedroads = integrateRoads(roadsinfo["data"], results, params["keywords_weights"])
    # selectedRoads = roadsPointsGroup(impactedroads)
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
                            # impactedRoads[road["id"]] = {"locations": Counter({road["location"]: road["contribution"]})}
                            impactedRoads[road["id"]] = {"locations": [(road["location"], road["contribution"])]}
                            # impactedRoads[road["id"]]["pointIds"] = Counter({road["pointId"]: road["contribution"]})
                            impactedRoads[road["id"]]["pointIds"] = [road["pointId"]]
                            impactedRoads[road["id"]]["weight"] = road["contribution"]
                            impactedRoads[road["id"]]["keywords"] = Counter(road["keywords"])

    for roadId, roadInfo in impactedRoads.items():
        for keyword, keywordContr in roadInfo["keywords"].items():
            roadInfo["keywords"][keyword] = keywordContr / len(roadInfo["pointIds"])
        countLoc = Counter([loc[0] for loc in roadInfo["locations"]])
        locDict = Counter({})
        for loc in roadInfo["locations"]:
            locDict.update(dict([loc]))
        for k, v in locDict.items():
            locDict[k] /= countLoc[k]
        roadInfo["locations"] = locDict
        roadInfo["weight"] /= len(locDict.keys())
        
    return impactedRoads


def merge2road(totalroad, newroad):
    # totalroad["pointIds"].update({newroad["pointId"]: newroad["contribution"]})
    totalroad["pointIds"].append(newroad["pointId"])
    totalroad["weight"] = totalroad["weight"] + newroad["contribution"]
    totalroad["locations"].append((newroad["location"], newroad["contribution"]))
    # totalroad["locations"].update({newroad["location"]: newroad["contribution"]})
    totalroad["keywords"].update(newroad["keywords"])   # Counter({"kw1": contrs})


def keywordContributions(keywords, keywords_weights, distance):
    KWContrs = {}
    disContrs = 0
    for kw in keywords:
        if kw in keywords_weights:
            sigKW = (keywords_weights[kw] - 50) * 2 + 50 * 1.5
        else:
            sigKW = 50
        disImpact = 200 / (distance)
        KWContrs[kw] = sigKW
        # disContrs += sigKW + disImpact
        disContrs += disImpact

    return disContrs, KWContrs


def roadsPointsGroup(roads):
    lenlist = []
    for roadid, roadinfo in roads.items():
        grouplist = pointsClustering(roadinfo["locations"])
        roadinfo["grouplist"] = grouplist
        lenlist.extend([gl[0] for gl in grouplist])
    threshold = sorted(lenlist)[-13:][0]
    selectedRoads = {}
    for roadid, roadinfo in roads.items():
        groupl = [{"locs": group[1], "weight": group[0]} for group in roadinfo["grouplist"] if group[0] > threshold]
        roadinfo["grouplist"] = groupl
        if len(groupl) != 0:
            selectedRoads[roadid] = groupl
    return selectedRoads


def pointsClustering(locations):
    db = DBSCAN(eps=200, min_samples=1, metric=get_distance).fit([list(map(float, loc.split(','))) for loc in list(locations.keys())])
    locgroup = list(zip(db.labels_, locations.items()))
    values = set(map(lambda x: x[0], locgroup))
    newlist = [dict([y[1] for y in locgroup if y[0] == x]) for x in values]
    return list(zip([sum(nl.values()) for nl in newlist], newlist))


def get_distance(array_1, array_2):
    lon_a = array_1[0]
    lat_a = array_1[1]
    lon_b = array_2[0]
    lat_b = array_2[1]
    radlat1 = radians(lat_a)
    radlat2 = radians(lat_b)
    a = radlat1 - radlat2
    b = radians(lon_a) - radians(lon_b)
    s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radlat1) * cos(radlat2)*pow(sin(b/2),2)))
    earth_radius = 6378137
    s = s * earth_radius
    return s
