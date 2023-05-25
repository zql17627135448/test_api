"""
@FileName  test_all_case.py
@Auther    百里
@description  零代码极限封装
"""
from pathlib import Path

import allure
import pytest
from commons.ddt_util import read_testcase_yaml
from commons.main_util import stand_case_flow
from commons.model_util import verify_yaml

#获得当前路径
from configs import setting

current_path = Path(__file__).parent
#找到所有的代表测试用例的yaml文件
yaml_case_list = current_path.glob("**/*.yaml")

#这是一个能够被pytest发现的类
@allure.epic(setting.allure_project_name)
class TestAllCase:
    pass

#创建测试用例函数
def create_testcase(yaml_path):

    @pytest.mark.parametrize("caseinfo", read_testcase_yaml(yaml_path))
    def test_func(self, caseinfo):
        global new_case
        #判断是否是流程用例
        if isinstance(caseinfo,list):
            for case in caseinfo:
                # 校验YAML格式
                new_case = verify_yaml(case, yaml_path.name)
                # 测试用例的标准化流程处理
                stand_case_flow(new_case)
        else:
            # 校验YAML格式
            new_case = verify_yaml(caseinfo,yaml_path.name)
            # 测试用例的标准化流程处理
            stand_case_flow(new_case)
        # Allure定制
        allure.dynamic.feature(new_case.feature)
        allure.dynamic.story(new_case.story)
        allure.dynamic.title(new_case.title)
    #返回测试用例函数
    return test_func

#循环得到所有的YAML文件名
for yaml_path in yaml_case_list:
    #反射：每循环一下向TestAllCase类中加入一个测试用例函数
    setattr(TestAllCase,"test_"+yaml_path.stem,create_testcase(yaml_path))

if __name__ == '__main__':
    print(yaml_case_list)