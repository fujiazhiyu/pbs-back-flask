# coding:utf-8

from flask import g, Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import sys


current_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:fish95520@localhost/chinavis17'
current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(current_app)


class MessageInfo(db.Model):
    """docstring for MessageInfo."""
    __tablename__ = 'testmessage'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    # md5 = db.Column(db.String(50))
    # content = db.Column(db.Text)
    theme = db.Column(db.Integer)
    keywords = db.Column(db.Text)
    phone = db.Column(db.String(30))
    conntime = db.Column(db.Integer)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    contacts = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, arg):
        super(MessageInfo, self).__init__()
        self.arg = arg

    def __repr__(self):
        # return '<theme %r, keywords %r, phone %r, recitime %r, lng %r, lat %r, contacts %r, id %r>' % (self.theme, self.keywords, self.phone, self.recitime, self.lng, self.lat, self.contacts, self.id)
        return '<theme %r, keywords %r, phone %r, conntime %r, lng %r, lat %r, contacts %r, id %r>' % (self.theme, self.keywords, self.phone, self.conntime, self.lng, self.lat, self.contacts, self.id)

    def format(self, *fields, method='UNPICK'):
        """格式化查询结果
        参数
        ---------
        self: Object
        *fields: list
            指定过滤的字段名称
        method: str
            指定处力 *fields 对应字段的方式, 'UNPICK': 舍弃, 'PICK': 保留

        返回值
        ---------
        dict
            格式化后的字段构成的字典

        示例
        ---------

        >>> result.format('phone', method='UNPICK')
        """
        formatRes = dict(id=self.id, theme=self.theme, keywords=self.keywords, phone=self.phone,
                         conntime=self.conntime, lng=self.lng, lat=self.lat, contacts=self.contacts)
        pick = dict()
        for f in fields:
            pick[f] = formatRes.pop(f, None)
        if method is 'PICK':
            return pick
        elif method is 'UNPICK':
            return formatRes
        else:
            return None


class Cluster(db.Model):
    """docstring for Cluster."""
    __tablename__ = 'keywords'
    md5 = db.Column(db.Text, primary_key=True)
    theme = db.Column(db.Text)
    keywords = db.Column(db.Text)
    contacts = db.Column(db.Text)
    count = db.Column(db.Integer)

    def __init__(self, arg):
        super(Cluster, self).__init__()
        self.arg = arg

    def __repr__(self):
        return '<md5 %r, theme %r, keywords %r, contacts %r, count %r>' % (self.md5, self.theme, self.keywords, self.contacts, self.count)
