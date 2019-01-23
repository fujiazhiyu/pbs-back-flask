# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import keywords
from flaskr import service


@keywords.route('/all', methods=['GET'])
def getKeywords():
    result = service.pickData(request.args.to_dict(flat=False), 'keywords')
    # [{"text": r, "weight": result[r], "html": {"draggable": "true"}} for r in result.keys()]
    if result["status"] == 0:
        result["records"] = []
        result.pop('info', None)
    return jsonify(result)


@keywords.route('/themes', methods=['GET'])
def getThemes():
    result = service.pickData(request.args.to_dict(flat=False), 'themes')
    return jsonify(result)
