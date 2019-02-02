from .asynCrawl import AsnycGrab
import math

keys = ("3a2acb37d52f6c8c0f5614bc1149dac7", "fb4db9e333acb1e68899d74062c2cf3a", "002bc3732803cef3c598618fd525cddf")
switchKey = 0


def crawlInfo(payloads):
    async_example = AsnycGrab(payloads, 5)
    async_example.eventloop()
    return async_example.results


def variableKeys():
    global switchKey
    switchKey = (switchKey + 1) % 3
    return {
        "base_url": "/v3/geocode/regeo?key=" + keys[switchKey],
        "batch_url": "https://restapi.amap.com/v3/batch?key=" + keys[switchKey]
    }


def generateURLS(points):
    options = []
    urls = []
    locations = []
    url_prefix = variableKeys()
    for i in range(len(points)):
        locations.append(str(points[i]["lng"]) + "," + str(points[i]["lat"]))
        if i % 20 == 19:
            sub_url = url_prefix["base_url"] + "&location=" + '|'.join(locations) + "&radius=250&extensions=all&batch=true&roadlevel=1"
            options.append({"url": sub_url})
            locations = []

        if i % 400 == 399:
            # urls.append({"ops": options})
            urls.append({"payload": {"ops": options}, "batch_url": url_prefix["batch_url"], "serial": str(math.floor(i / 400)) })
            options = []

    if len(locations) != 0:
        sub_url = url_prefix["base_url"] + "&location=" + '|'.join(locations) + "&radius=250&extensions=all&batch=true&roadlevel=1"
        options.append({"url": sub_url})
        locations = []

    if len(options) != 0:
        urls.append({"payload": {"ops": options}, "batch_url": url_prefix["batch_url"], "serial": str(math.floor(i / 400)) })
        options = []

    return urls


if __name__ == '__main__':
    points =  [ { "id": 483153, "keywords": "提额;银行;信用卡;申请", "lat": 39.883453, "lng": 116.453072 }, { "id": 483964, "keywords": "提额;银行;信用卡;申请", "lat": 39.876114, "lng": 116.464699 }, { "id": 483968, "keywords": "提额;银行;信用卡;申请", "lat": 39.876114, "lng": 116.464699 }, { "id": 483982, "keywords": "提额;银行;信用卡;申请", "lat": 39.876114, "lng": 116.464699 }, { "id": 483986, "keywords": "提额;银行;信用卡;申请", "lat": 39.876114, "lng": 116.464699 }, { "id": 3171516, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.881992, "lng": 116.482254 }, { "id": 3171517, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.881992, "lng": 116.482254 }, { "id": 3172207, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.880749, "lng": 116.461052 }, { "id": 3172208, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.880844, "lng": 116.456879 }, { "id": 3172209, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.880749, "lng": 116.461052 }, { "id": 3172210, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.880844, "lng": 116.456879 }, { "id": 3172211, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.877468, "lng": 116.459023 }, { "id": 3173780, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.871708, "lng": 116.461327 }, { "id": 3173785, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.871708, "lng": 116.461327 }, { "id": 3207695, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.89008, "lng": 116.476326 }, { "id": 3208155, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.864464, "lng": 116.444992 }, { "id": 3208159, "keywords": "现金;积分兑换;网址;账户;用户;清零;银行;逾期", "lat": 39.864464, "lng": 116.444992 } ]
    roadsInfo = crawlInfo(generateURLS(points))
    print(roadsInfo)
