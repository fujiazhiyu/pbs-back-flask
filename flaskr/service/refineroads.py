# coding:utf-8
import json
from math import *
import os


def refineRoads(selectedRoads):
    with open('instance/simpleRoadsInfowithId.geojson', 'r') as fr:
        geojson = json.loads(fr.read())
        # roadid: coords
        roadiddict = {}
        for road in geojson["features"]:
            if "id" in road["properties"]:
                roadiddict[road["properties"]["id"]] = road["geometry"]["coordinates"]

        refineroadsdict = {}
        for roadid, roadpieces in selectedRoads.items():
            if roadid not in roadiddict:
                print("not found...", roadid)
                continue
            # roadid 这条路的片段的refine结果
            refineroadpieces = []
            for rp in roadpieces:
                closestidxlist = []
                for loc in rp["locs"].keys():
                    closestidx = getClosestPoint(list(map(float, loc.split(','))), roadiddict[roadid])
                    closestidxlist.append(closestidx)
                    if len(roadiddict[roadid]) - 1 > closestidx:
                        closestidxlist.append(closestidx + 1)
                    if closestidx > 0:
                        closestidxlist.append(closestidx - 1)

                # 一个locs对应的road point idxs, 取首尾idx即可
                closestidxlist.sort()
                if len(closestidxlist) == 0:
                    print("len(closestidxlist) == 0...", roadid)
                refineroadpieces.append({"weight": rp["weight"], "coordinates": roadiddict[roadid][closestidxlist[0]:closestidxlist[-1]+1]})

            refineroadsdict[roadid] = refineroadpieces

        return refineroadsdict


def getClosestPoint(point, roadpoints):
    closestdis = 1000
    closestidx = -1
    for rpidx in range(len(roadpoints)):
        newdis = get_distance(point, roadpoints[rpidx])
        if newdis < closestdis:
            closestdis = newdis
            closestidx = rpidx

    if closestidx == -1:
        print("no closest??", point, roadpoints)
    return closestidx


def get_distance(array_1, array_2):
    lon_a = array_1[0]
    lat_a = array_1[1]
    lon_b = array_2[0]
    lat_b = array_2[1]
    radlat1 = radians(lat_a)
    radlat2 = radians(lat_b)
    a = radlat1 - radlat2
    b = radians(lon_a) - radians(lon_b)
    s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radlat1) * cos(radlat2) * pow(sin(b / 2), 2)))
    earth_radius = 6378137
    s = s * earth_radius
    return s
