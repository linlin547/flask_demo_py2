# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://li:123456@localhost/Test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 15 # 数据库连接池
db = SQLAlchemy(app)


class Interface_config(db.Model):
    __tablename__ = 'config_interface' # 接口配置记录表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),index=True,unique=True) #接口名称
    url = db.Column(db.String(80)) # 接口地址
    param = db.Column(db.String(120)) # 接口参数
    expect_data = db.Column(db.String(120)) # 预期结果

    def __init__(self, name, url, param, expect_data):
        self.name = name
        self.url = url
        self.param = param
        self.expect_data = expect_data

    def __repr__(self):
        return '<User %r>' % self.name

class Interface_result(db.Model):
    __tablename__ = 'interface_result' # 接口结果表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),index=True) #接口名称
    res_data = db.Column(db.String(80)) # 接口返回数据
    status = db.Column(db.Integer) # 状态 0：成功，1：失败
    faile_reason = db.Column(db.String(120)) # 失败原因

    def __init__(self, name, res_data, status, faile_reason):
        self.name = name
        self.res_data = res_data
        self.status = status
        self.faile_reason = faile_reason

    def __repr__(self):
        return '<User %r>' % self.name

# db.create_all()