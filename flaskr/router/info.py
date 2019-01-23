# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import infos
from flaskr import service


@infos.route('/contacts', methods=['GET'])
def getDataset():
    result = service.pickContacts(request.args.to_dict(flat=False))
    return jsonify(result)
