"""
@FileName  base_url_util.py
@Auther    百里
@description  读取基础路径的工具类
"""
from iniconfig import IniConfig

def load_ini():
    ini = IniConfig("./pytest.ini")
    if "base_url" not in ini:
        return {}
    else:
        return dict(ini["base_url"].items())

if __name__ == '__main__':
    print(load_ini())
