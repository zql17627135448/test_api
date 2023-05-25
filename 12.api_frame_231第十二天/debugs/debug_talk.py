"""
@FileName  debug_talk.py
@Auther    百里
@description  热加载的类，其实也是框架的扩展口
jmeter:beanshell，postman：前后置脚本
"""
import base64
import hashlib
import time
import rsa
import yaml

from commons.base_url_util import load_ini
from configs import setting

class DebugTalk:

    # 读取extract.yaml
    def read_extract(self,key):
        with open(setting.extract_file_name, encoding="utf-8", mode="r") as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data[key]

    #随机数
    def get_times(self):
        return int(time.time())

    #获取pytest.ini中的base_url中的值
    def get_base_url(self,key):
       return load_ini()[key]

    #MD5加密
    def md5_encode(self,args):
        # 把变量转化为utf-8的编码格式
        utf8_str = str(args).encode("utf-8")
        #md5加密
        md5_value = hashlib.md5(utf8_str).hexdigest()
        return md5_value

    #Base64加密
    def base64_encode(self,args):
        # 把变量转化为utf-8的编码格式
        utf8_str = str(args).encode("utf-8")
        # bas64加密
        base64_value = base64.b64encode(utf8_str).decode(encoding="utf-8")
        return base64_value

    #生成RSA的公钥和私钥
    # def create_key(self):
    #     #生成公钥和私钥
    #     (public_key,private_key)=rsa.newkeys(nbits=1024)
    #     #保存公钥
    #     with open("./public.pem","w+") as f:
    #         f.write(public_key.save_pkcs1().decode())
    #     # 保存私钥
    #     with open("./private.pem", "w+") as f:
    #         f.write(private_key.save_pkcs1().decode())

    #RSA加密
    def rsa_encode(self,args):
        #获取到公钥
        with open("./debugs/public.pem","r") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        #把变量转化成utf-8编码格式
        utf8_str = str(args).encode("utf-8")
        # 把字符串进行rsa加密
        byte_value = rsa.encrypt(utf8_str,pubkey)
        #把字节类型的值转化成字符串的值
        rsa_str = base64.b64encode(byte_value).decode("utf-8")
        return rsa_str

if __name__ == '__main__':
    print(DebugTalk().rsa_encode("admin"))




