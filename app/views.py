#!flask/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json,logging,time

from flask import Flask, jsonify, make_response, request, url_for, render_template, flash, redirect
from flask import abort
from Mysql_operator.operator_obj import Operator_Work
from Mysql_operator.mysql_manage import Mysql_Manage
from app import app
from app.forms import LoginForm

"""
    声明log对象
"""
handler = logging.FileHandler('./log/%s.log' % time.strftime('%Y-%m-%d',time.localtime(time.time())), encoding='UTF-8')

handler.setLevel(logging.DEBUG)

logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)

app.logger.addHandler(handler)
# app.logger.removeHandler(handler)

"""
    声明数据库操作对象
"""
mm_obj = Mysql_Manage()
"""
    声明全局参数
"""
post_params={}

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/tt', methods=['POST'])
def do_post():

    if not request.json:
        return "请求json数据不能为空！", 400
    if not 'url' in request.json or not 'param' in request.json:
        return "请求 url 或者 param 数据不存在！", 400
    try:
        post_params = {
            'name': request.json['name'],
            'url': request.json['url'],
            'param': request.json['param'],
            'expect_data': request.json['expect_data']
        }
        app.logger.info(u"拼接post参数:"+str(json.dumps(post_params,ensure_ascii=False).decode('utf-8')))

    except Exception,e:
        # app.logger.error(u"组装json数据报错:"+str(e))
        print e
    try:
        OW = Operator_Work(post_params)
        if mm_obj.insert_data(OW.init_config()) == 0:
            return "接口名称重复"
        if mm_obj.insert_data(OW.init_config()) == 1 or mm_obj.insert_data(OW.init_result())==1:
            return "数据库插入信息报错"

        # app.logger.info(u"入库完成!")
        return str({"status":1})
    except Exception,e:
        # app.logger.error(u"信息入库报错："+str(e))
        print e
        return str({"status":0})
# @app.route('/', methods=['GET'])
# def get_one():
#     if not request.args['LastName']:
#         abort(400)
#     get_LastName= request.args['LastName']
#     #得到表中所有的数据
#     ids = Student.query.all()
#     #使用filter找到指定项目
#     get = Student.query.filter_by(LastName = get_LastName).first()
#     #获取表成员属性
#     ret = 'LastName=%s \n FirstName=%s \n Address=%s' % (get.LastName, get.FirstName, get.Address,)
#     return ret

@app.route('/test/api/resultss', methods=['POST'])
def create_task():

    if not request.json or not 'test' in request.json:
        abort(400)
    res = {"res_data": {"res_data": {"a": 3, "b": 4}}, "status": 1, "faile_reason": "其他原因!"}
    return jsonify({'res': res}), 200


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [i for i in map(make_public_task, tasks).__iter__()]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = [i for i in filter(lambda t: t['id'] == task_id, tasks).__iter__()]
    except Exception as e:
        print(e)
        task = ""
    if len(task) == 0:
        abort(404)
    return jsonify({'task': [i for i in map(make_public_task, task)]})

# @app.route('/todo/api/v1.0/tasks1', methods=['POST'])
# def create_task():
#
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     app.logger.info(task)
#     tasks.append(task)
#     return jsonify({'task': [i for i in map(make_public_task, tasks).__iter__()]}), 201


@app.route('/index/<param>')
def index_users(param):
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = '%s'%param,
        user = user,
        posts = posts)

@app.route('/l_test', methods = ['GET', 'POST'])
def interface_conf():
    """
            接口配置信息入库
    :return:
    """
    post_params = {
        'name': request.values.get("inter_name"),
        'url': request.values.get("inter_url"),
        'param': request.values.get("inter_param"),
        'expect_data': request.values.get("inter_expect"),
        'req_type': request.values.get("inter_type")
    }

    # 重定向到带参数的地址
    # if request.values.get("inter_name"):
    #     return redirect(url_for('index_users',param="aaaa")) # 重定向到有参数的url,用url_for(路由对应函数名，参数)
    if post_params.get("name")  and  post_params.get("url"):
        app.logger.info(u"待入库信息:" + json.dumps(post_params))
        try:
            OW = Operator_Work(post_params)
            insert_config_res = mm_obj.insert_data(OW.init_config())

            if insert_config_res == 0:
                return "接口名称重复"
            if insert_config_res == 1:
                return "数据库插入信息报错"
            app.logger.info(u"入库完成!")

        except Exception,e:
            app.logger.error(u"信息入库报错："+str(e))
            return str({"status":0})
    return render_template('interface_config.html',
        title = u'接口参数保存',
        form = request.form)