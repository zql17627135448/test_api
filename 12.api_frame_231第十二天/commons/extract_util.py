"""
@FileName  extract_util.py
@Auther    百里
@description  ... 
"""
import copy
import json
import re
from dataclasses import asdict
import jsonpath
import yaml
from commons.model_util import CaseInfo
from commons.yaml_util import write_extract_yaml
from debugs.debug_talk import DebugTalk


class ExtractUtil:

    # 提取变量
    def extract(self, response, var_name: str, attr_name: str, expr: str, index: int):
        # 1.深拷贝一个response（深拷贝，浅拷贝）
        resp = copy.deepcopy(response)
        # 深拷贝：对对象的地址进行拷贝，新拷贝的对象和原来的对象地址不一样，修改新拷贝的对象不会改变原来的对象。
        # 浅拷贝：对对象的值进行拷贝，新拷贝的对象和原来的对象地址一样，修改新(旧)拷贝的对象都会改变原来的对象。
        # 2.把json()改成一个属性
        try:
            resp.json = resp.json()
        except Exception:
            resp.json = {"msg": "response is not json"}
        # 3.通过属性反射获取到属性的数据
        data = getattr(resp, attr_name)
        # print("data %s "%dict(data))
        # 判断提取方式
        # 正则提取：（只能提取字符串）
        # re.findall
        # JSONPATH提取：（只能提取字典格式）
        # jsonpath.jsonpath()
        if expr.startswith("$"):  # jsonpath提取
            lis = jsonpath.jsonpath(dict(data), expr)
        else:
            lis = re.findall(expr, data)
        # 通过下标取值
        if lis:
            var_value = lis[index]
        else:
            var_value = "not extract data"
        # 把提取的数据写入extarct.yaml
        write_extract_yaml({var_name: var_value})

    # 使用变量(给我一个字典，替换之后，再返回一个字典)
    def change(self, data_dict: dict):
        # 1.把dict字典转化成一个字符串。
        yaml_str = yaml.dump(data_dict)
        # 2.替换
        # new_str = Template(str).safe_substitute(read_extract_yaml())
        new_yaml_str = ExtractUtil().hot_load_replace(yaml_str)
        # 3.转回CaseInfo的对象
        data_dict = yaml.safe_load(new_yaml_str)
        return data_dict

    # 热加载,就是让yaml能够调用python方法
    def hot_load_replace(self, yaml_str):
        # 定义一个匹配${函数名(变量名1, 变量名2....)}表达式的正则
        regexp = "\\$\\{(.*?)\\((.*?)\\)\\}"
        # 通过正则取匹配yaml里面的表达式，得到函数名和参数
        fun_list = re.findall(regexp, yaml_str)
        # 循环,f[0]就是函数名，f[1]参数名
        for f in fun_list:
            if f[1] == "":  # 没有参数
                new_value = getattr(DebugTalk(), f[0])()
            else:  # 有参数,可能一个，也可能多个。
                new_value = getattr(DebugTalk(), f[0])(*f[1].split(","))
            # 判断如果是数字类型的字符串，那么加上单引号
            if isinstance(new_value, str) and new_value.isdigit():
                new_value = "'" + new_value + "'"
            # 拼接旧值
            old_value = "${" + f[0] + "(" + f[1] + ")}"
            # 把旧的字符串替换成新的字符串
            yaml_str = yaml_str.replace(old_value, str(new_value))
        return yaml_str
