#!flask/bin/python
# -*- coding: utf-8 -*-
import requests,json

import sql_manage as sm

class Operator_Work:

    def __init__(self,post_params):
        self.post_params = post_params

    def init_config(self):
        # 初始化配置表数据
        param = self.post_params.get('param')
        expect_data = self.post_params.get('expect_data')
        if isinstance(param,dict):
            param = json.dumps(self.post_params.get('param'))
        if isinstance(expect_data, dict):
            expect_data = json.dumps(self.post_params.get('expect_data'))

        conf_sql = sm.insert_interface_conf % (self.post_params.get('name'), self.post_params.get('url'), str(param),expect_data, self.post_params.get('req_type'))
        return conf_sql

    def init_result(self):
        # 初始化结果表数据
        try:
            get_url_data = requests.post(url=self.post_params.get('url'), json=self.post_params.get('param')).json()
        except Exception,e:
            print e
            return 0
        res_data = get_url_data.get('res').get('res_data')
        faile_reason = get_url_data.get('res').get('faile_reason')
        if isinstance(res_data,dict):
            res_data = json.dumps(res_data)
        if isinstance(faile_reason,dict):
            faile_reason = json.dumps(faile_reason)
        result_sql = sm.insert_interface_result % (self.post_params.get('name'), str(res_data), int(get_url_data.get('res').get('status')),faile_reason)
        return result_sql
