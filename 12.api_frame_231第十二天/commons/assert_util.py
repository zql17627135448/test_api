"""
@FileName  assert_util.py
@Auther    百里
@description  ... 
"""
import copy
import json

import pymysql
import yaml

from configs import setting


class AssertUtil:
    #创建数据库链接，pymysql和mysqlclient
    def create_connection(self):
        self.conn = pymysql.connect(
            user=setting.db_user,
            password=setting.db_password,
            host=setting.db_host,
            database=setting.db_database,
            port=setting.db_port
        )
        return self.conn

    #执行SQL语句
    def execute_sql(self,sql):
        #创建链接
        conn = self.create_connection()
        # 创建游标
        cs = conn.cursor()
        #执行sql
        cs.execute(sql)
        #取值
        value = cs.fetchone()
        #关闭
        cs.close()
        conn.close()
        return value

    #处理所有的断言
    def assert_all(self,resp,assert_key,assert_value):
        # 1.深拷贝一个response（深拷贝，浅拷贝）
        resp = copy.deepcopy(resp)
        # 2.把json()改成一个属性
        try:
            resp.json = resp.json()
        except Exception:
            resp.json = {"msg": "response is not json"}
        # 3.循环断言内容
        for msg,data in assert_value.items():
            sj,yq = data[0],data[1]
            # 4.通过属性反射获取到属性的数据
            try:
                sj_data = getattr(resp, sj)
            except Exception:
                sj_data = sj
            #实际结果的类型从字典转化成字符串
            if isinstance(sj_data,dict):
                sj_data = yaml.dump(sj_data,allow_unicode=True)
            # 5.断言
            match assert_key:
                case "equals":
                    assert yq==sj_data,msg
                case "contains":
                    assert yq in sj_data,msg
                case "db_equals":
                    value = self.execute_sql(yq)
                    if value:
                        assert value[0] == sj_data,msg
                case "db_contains":
                    value = self.execute_sql(yq)
                    if value:
                        assert value[0] in sj_data,msg