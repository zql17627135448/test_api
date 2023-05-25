import yaml

#读取extract.yaml
from configs import setting

def read_extract_yaml():
    with open(setting.extract_file_name,encoding="utf-8",mode="r") as f:
        value  = yaml.safe_load(f)
        return value

#写入extract.yaml
def write_extract_yaml(data):
    with open(setting.extract_file_name,encoding="utf-8",mode="a+") as f:
        yaml.safe_dump(data, stream=f,allow_unicode=True)

#清空extract.yaml
def clear_extract_yaml():
    with open(setting.extract_file_name, encoding="utf-8", mode="w") as f:
        pass