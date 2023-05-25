import re
import time
from pathlib import Path

import jsonpath as jsonpath
import pytest

from commons.request_util import RequestUtil
from commons.yaml_util import write_extract_yaml, read_extract_yaml, read_testcase_yaml

#获取当前路径
test_path = str(Path(__file__).parent)

class TestApi2:

    #测试pipwind首页接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/test_phpwind_start.yaml"))
    def test_phpwind_start(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]

        res = RequestUtil(caseinfo).send_all_request(method=method,url=url)
        value =  re.findall('name="csrf_token" value="(.*?)"', res.text,)
        token_data = {"csrf_token": value[0]}
        write_extract_yaml("./extract.yaml", token_data)

    # 测试pipwind首页接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/test_phpwind_login.yaml"))
    def test_phpwind_login(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        headers = caseinfo["request"]["headers"]
        data = caseinfo["request"]["data"]
        data["csrf_token"] = read_extract_yaml("./extract.yaml","csrf_token")

        res = RequestUtil(caseinfo).send_all_request(method=method,url=url,headers=headers,data=data)
        print(res.json())

    #获取token接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/get_token.yaml"))
    def test_get_token(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        params = caseinfo["request"]["params"]

        res = RequestUtil(caseinfo).send_all_request(method=method,url=url,
                     params=params)
        print(res.json())
        value = jsonpath.jsonpath(res.json(), "$.access_token")

        token_data = {"access_token": value[0]}
        write_extract_yaml("./extract.yaml", token_data)

    #文件上传接口
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml(test_path+"/test_file_upload.yaml"))
    def test_file_upload(self,caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        params = caseinfo["request"]["params"]
        params["access_token"] = read_extract_yaml("./extract.yaml","access_token")
        files = caseinfo["request"]["files"]
        files["media"] = open(files["media"],"rb")

        res = RequestUtil(caseinfo).send_all_request(method=method,url=url,
                      params=params,
                      files=files)
        print(res.json())