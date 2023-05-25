"""
@FileName  setting.py
@Auther    百里
@description  全局配置
"""

#数据库的配置
db_user="sdm723416659"
db_password="Msjy123456"
db_host="sdm723416659.my3w.com"
db_database="sdm723416659_db"
db_port=3306

#公共参数,默认为{}
globawl_args = {
    "application": "app",
    "application_client_type": "h5"
}

#存放中间变量的文件名
extract_file_name = "extract.yaml"

#Allure报告中项目名称
allure_project_name = "码尚教育B2C接口自动化测试"