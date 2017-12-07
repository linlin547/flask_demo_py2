#!flask/bin/python
# -*- coding: utf-8 -*-
import requests

from rub.DB_Config import Interface_config, Interface_result, db


class Operator_Work:
    def __init__(self,post_params):
        self.post_params = post_params

    def init_config(self):
        # 初始化配置表数据
        init_config_data = Interface_config(self.post_params.get('name'), self.post_params.get('url'), str(self.post_params.get('param')),
                                            self.post_params.get('expect_data'))
        return init_config_data

    def init_result(self):
        # 初始化结果表数据
        try:
            get_url_data = requests.post(url=self.post_params.get('url'), json=self.post_params.get('param')).json()
        except Exception,e:
            print e
        init_result_data = Interface_result(self.post_params.get('name'), str(get_url_data.get('res').get('res_data')), int(get_url_data.get('res').get('status')),
                                            get_url_data.get('res').get('faile_reason'))
        return init_result_data

    def add_data(self,add_obj):
        # 添加数据
        db.session.add(add_obj)

    def delete_data(self,del_obj):
        # 删除数据
        db.session.delete(del_obj)
    def commit_data(self):
        # 提交数据
        db.session.commit()