# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import paths
# from flask_cors import cross_origin
from flaskr.service import service


@paths.route('/recommend', methods=['POST'])
# @cross_origin(supports_credentials=True)
def postPaths():
    params = request.get_json()
    results = service.pickData(params, 'recommend')
    print(len(results["data"]))
    return jsonify(params)
