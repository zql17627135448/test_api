"""
@FileName  ddt_util.py
@Auther    百里
@description  ... 
"""
import yaml
from commons.request_util import logger

#读取测试用例
def read_testcase_yaml(yaml_path):
    with open(yaml_path,encoding="utf-8",mode="r") as f:
        case_list  = yaml.safe_load(f)
        if len(case_list)>=2: #流程用例
            return [case_list]  #[[{},{}]]  解包  [{},{}]
        else:
            if "parametrize" in dict(*case_list).keys():
                new_caseinfo = ddts(*case_list,yaml_path.name)
                return new_caseinfo  # [{},{},{}]  #数据驱动用例   解包之后：{},{},{}
            else:
                return case_list    #[{}]  #单接口用例，解包{}

#处理parametrize数据驱动，{parametrize}改造成[{},{},{}]
def ddts(case: dict,yaml_name):
    param_list = case["parametrize"]
    if param_list:   #判断parametrize不为空
        #判断名称和数据的长度必须一致
        name_length = len(param_list[0])
        for p in param_list:
            if len(p)!=name_length:
                logger.error(yaml_name+"：parametrize数据驱动中数据或名称长度不一致\n")
                break
        else:
            #如果长度没有问题
            new_caseinfo_list = []
            #把字典转化为字符串,因为只有字符串才可以替换
            case_str = yaml.dump(case)
            #循环
            for x in range(1,len(param_list)): #行[[],[],[],[]]len(param_list)
                raw_caseinfo = case_str  #执行之前先保存一份case
                for y in range(0,name_length): #列name_length
                    #处理数据类型，如果是数字类型的字符串则加一对单引号
                    if isinstance(param_list[x][y], str) and param_list[x][y].isdigit():
                        param_list[x][y] = "'" + param_list[x][y] + "'"
                    #替换
                    raw_caseinfo = raw_caseinfo.replace("$ddt{"+param_list[0][y]+"}",str(param_list[x][y]))
                #加入新的list中
                raw_case_dict = yaml.safe_load(raw_caseinfo)
                raw_case_dict.pop("parametrize")
                new_caseinfo_list.append(raw_case_dict)
            return new_caseinfo_list
    else:
        return [case]

