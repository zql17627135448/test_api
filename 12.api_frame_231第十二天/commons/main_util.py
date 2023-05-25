"""
@FileName  main_util.py
@Auther    百里
@description  标准化用例处理流程
"""
import traceback
from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model_util import CaseInfo
from commons.request_util import logger, RequestUtil

#创始化一个ExtractUtil的对象
eu = ExtractUtil()
#初始化一个RequestUtil的对象
ru = RequestUtil()
#初始化一个AssertUtil的对象
au = AssertUtil()

def stand_case_flow(new_case: CaseInfo):
    # 打印请求参数日志
    logger.info("模块>接口>用例：" + str(new_case.feature) + ">" + str(new_case.story) + ">" + str(new_case.title))
    # 发送请求获得响应
    resp = ru.send_all_request(**eu.change(new_case.request))
    # 如果yaml中有extract关键字，那么则提取变量
    if new_case.extract:
        for extarct_key, extarct_value in new_case.extract.items():  # 对extract进行循环
            eu.extract(resp, extarct_key,*extarct_value)  # 提取变量
    #如果yaml中有validate关键字并且不为None，那么则调用断言方法
    try:
        if new_case.validate:
            # 热加载：交换变量(使用变量)
            for assert_key,assert_value in eu.change(new_case.validate).items():
                au.assert_all(resp,assert_key,assert_value)
            # 写入日志
            logger.info("接口请求成功! \n")
        else:
            # 写入日志
            logger.warning("没有断言! \n")
    except Exception as e:
        #写入日志
        logger.error("失败! \n %s" % str(traceback.format_exc()))
        raise
