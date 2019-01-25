# coding:utf-8

from flask import (jsonify, request)
from flaskr.router import infos
from flaskr.service import service


@infos.route('/contacts', methods=['GET'])
def getDataset():
    result = service.pickData(request.args.to_dict(flat=False), 'contacts')
    return jsonify(result)
