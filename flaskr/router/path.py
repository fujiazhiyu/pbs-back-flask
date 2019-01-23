# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import paths
# from flask_cors import cross_origin
from flaskr import service
import sys


@paths.route('/recommend', methods=['POST'])
# @cross_origin(supports_credentials=True)
def postPaths():
    # print(request.args.to_dict(flat=False), file=sys.stdout)
    params = request.get_json()
    print(params)
    return jsonify(params)
