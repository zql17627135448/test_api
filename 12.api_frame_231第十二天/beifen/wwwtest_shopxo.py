from pathlib import Path

import pytest
import requests

from commons.request_util import RequestUtil
from commons.yaml_util import write_extract_yaml, read_extract_yaml, read_testcase_yaml

#获取当前路径
test_path = str(Path(__file__).parent)

class TestShopxo:

    #测试首页接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/test_2_query.yaml"))
    def test_index(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        params = caseinfo["request"]["params"]
        res = RequestUtil(caseinfo).send_all_request(method=method,url=url,params=params)
        print(res.json())


    # 商品详情接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/product_detail.yaml"))
    def test_product_detail(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        params = caseinfo["request"]["params"]
        json = caseinfo["request"]["json"]
        res = RequestUtil(caseinfo).send_all_request(method=method,url=url, params=params,json=json)
        print(res.json())

    #登陆接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/login_shopxo.yaml"))
    def test_login(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        params = caseinfo["request"]["params"]
        json = caseinfo["request"]["json"]
        res = RequestUtil(caseinfo).send_all_request(method=method,url=url, params=params, json=json)
        print(res.json())
        token_data = {"token":res.json()["data"]["token"]}
        write_extract_yaml("./extract.yaml",token_data)

    # 订单列表接口(需要登陆)
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/test_1_add.yaml"))
    def test_order_list(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        yaml_params = caseinfo["request"]["params"]
        json = caseinfo["request"]["json"]
        params = {
            "token":read_extract_yaml("./extract.yaml","token")
        }
        params.update(yaml_params)
        res = RequestUtil(caseinfo).send_all_request(method=method,url=url, params=params, json=json)
        print(res.json())

