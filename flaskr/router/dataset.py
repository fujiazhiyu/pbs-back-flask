# coding:utf-8
from flask import (jsonify, request)
from flaskr.router import datasets
from flaskr.service import service
import time


@datasets.route('/selection', methods=['GET'])
def getDataset():
    # result = service.pickDataset(request.args)
    result = {
        "status": "success",
        "records": [{"id": 0, "text": "weekday"}, {"id": 1, "text": "weekend"}]
    }
    return jsonify(result)


@datasets.route('/hello', methods=['GET'])
def hello():
    return 'hello'


@datasets.route('/hellowait', methods=['GET'])
def hellowait():
    time.sleep(5)
    return 'hellowait'
