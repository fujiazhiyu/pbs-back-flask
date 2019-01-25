# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import messages
# from flask_cors import cross_origin
from flaskr.service import service
import sys


@messages.route('/points', methods=['GET'])
# @cross_origin(supports_credentials=True)
def getDataset():
    # print(request.args.to_dict(flat=False), file=sys.stdout)
    result = service.pickData(request.args.to_dict(flat=False), 'messages')
    return jsonify(result)
