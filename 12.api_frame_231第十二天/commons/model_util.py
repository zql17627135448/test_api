"""
@FileName  model_util.py
@Auther    百里
@description  封装的规范YAML以及校验YAML的类
"""

from dataclasses import dataclass
from commons.request_util import logger

#dataclass是类在实例化过程中(调用__init__方法时给属性赋值)自动传参和自动校验的工具类
@dataclass
class CaseInfo:
    #必填
    feature: str
    story: str
    title: str
    request: dict
    validate: dict
    #选填
    extract: dict = None
    parametrize: list = None

#校验YAML格式
def verify_yaml(case: dict,yaml_name):
    try:
        new_case = CaseInfo(**case)
        return new_case
    except Exception:
        logger.error(yaml_name+"：YAML格式不符合框架规则\n")
        raise Exception("YAML格式不符合框架规则！")
