# -*- coding: utf-8 -*-

# 接口配置信息入库
insert_interface_conf = "insert into  config_interface(name,url,param,expect_data,req_type) values('%s','%s','%s','%s','%s')"
# 接口结果返回信息入库
insert_interface_result = "insert into  interface_result(name,res_data,status,faile_reason) values('%s','%s','%d','%s')"