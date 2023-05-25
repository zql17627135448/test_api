import logging

import requests

#生成日志对象
from configs import setting

logger = logging.getLogger(__name__)

class RequestUtil:

    #类变量和实例变量
    sess = requests.session()

    #统一请求接口封装，self是当前类的对象，和java中的this一样。
    def send_all_request(self,**kwargs):
        #处理参数
        for args_key,args_value in kwargs.items():
            # 处理公共参数
            if args_key=="params":
                kwargs["params"].update(setting.global_args)
            #处理files
            try:
                if args_key=="files":
                    for key,value in args_value.items():
                        args_value[key]=open(value,"rb")
            except Exception:
                logger.error("文件路径找不到!\n")
                raise
            #打印请求参数日志
            logger.info("请求"+args_key+"参数：%s"%args_value)
        #发送请求
        res = RequestUtil.sess.request(**kwargs)
        if "json" in res.headers.get("Content-Type"):
            logger.info("响应正文：%s"%res.json())
        else:
            # 打印响应参数日志
            logger.info("响应正文：太长暂不显示")

        return res