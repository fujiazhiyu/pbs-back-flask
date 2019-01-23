# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import areas
from flaskr import service


@areas.route('/preset', methods=['GET'])
def getDataset():
    result = {
        "status": "success",
        "records": [{"id": 0, "text": "朝阳区"},
                    {"id": 1, "text": "东城区"},
                    {"id": 2, "text": "西城区"},
                    {"id": 3, "text": "丰台区"},
                    {"id": 4, "text": "顺义区"},
                    {"id": 5, "text": "大兴区"},
                    {"id": 6, "text": "石景山区"},
                    {"id": 7, "text": "门头沟区"},
                    {"id": 8, "text": "海淀区"},
                    {"id": 9, "text": "昌平区"},
                    {"id": 10, "text": "房山区"},
                    {"id": 11, "text": "通州区"}]
    }
    return jsonify(result)


@areas.route('/custom', methods=['POST'])
def saveCustomArea():
    """设置自己的area"""
    pass
