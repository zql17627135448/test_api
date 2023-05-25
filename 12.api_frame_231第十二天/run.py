import os
import shutil
import time
import pytest

if __name__ == '__main__':
    pytest.main(["-vs"])
    time.sleep(3)
    os.system("allure generate ./temps -o ./reports --clean")
    #time.sleep(3)
    #os.system("allure open ./reports")
    #拷贝日志
    #shutil.move("logs/frame.log","logs/frame_"+str(int(time.time()))+".log")