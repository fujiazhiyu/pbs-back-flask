# coding:utf-8

from flask import Blueprint
# dataset selection
datasets = Blueprint('datasets',  __name__, url_prefix='/api/datasets')
# area selection or commit
areas = Blueprint('areas', __name__, url_prefix='/api/areas')
# themes keywords and keywords selection
keywords = Blueprint('keywords', __name__, url_prefix='/api/keywords')
# time period
time = Blueprint('time', __name__, url_prefix='/api/time')
# contacts details and other infos
infos = Blueprint('infos', __name__, url_prefix='/api/infos')
# messages from messagesinfo - mongodb
messages = Blueprint('messages', __name__, url_prefix='/api/messages')
# recommend paths according to user selected params
paths = Blueprint('paths', __name__, url_prefix='/api/paths')
from flaskr.router import dataset
from flaskr.router import area
from flaskr.router import keyword
from flaskr.router import info
from flaskr.router import message
from flaskr.router import path
