import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前工作目录更改为脚本所在的目录
sys.path.append(current_dir)
import platform
import glob
from log_utils import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text, delete, func
from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, SmallInteger, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import pandas as pd


class WCGClass:

    def __init__(self):
        # 获取所有仓库的公共目录
        self.current_file_path = os.path.abspath(__file__)
        self.current_dir = os.path.dirname(self.current_file_path)
        self.common_dir = os.path.dirname(self.current_dir)

    def get_os(self):
        os_name = platform.system()
        if os_name == 'Windows':
            return 'Windows'
        elif os_name == 'Linux':
            return 'Linux'
        elif os_name == 'Darwin':
            return 'Mac'
        else:
            return 'Unknown OS'
    
    def get_project_dir(self, current_path):
        # 判断一个目录是否是项目的根目录。这里使用了一个简单的判定条件：根目录下是否存在一个名为".git"的目录。
        # 你可以根据你的项目特点修改这个条件。
        def is_root(path):
            return '.git' in os.listdir(path)

        # 获取本.py脚本所在的目录的绝对路径
        # script_absolute_path = os.path.abspath(__file__)
        script_absolute_path = os.path.abspath(current_path)
        script_dir = os.path.dirname(script_absolute_path)
        # 从起始目录开始，递归地向上查找
        while not is_root(script_dir):
            parent_path = os.path.dirname(script_dir)
            if parent_path == script_dir:
                raise Exception("项目根目录没有找到")
            script_dir = parent_path
        return script_dir
    
    def df2csv(self, df, csv_name):
        df.to_csv(f'{csv_name}.csv', index=False)
        return f'{csv_name}.csv'

    def regular_find_folder(self, base_path, pattern):
        # 使用 glob 模块来进行模糊匹配
        search_pattern = os.path.join(base_path, pattern)
        folders = glob.glob(search_pattern)
        if folders:
            return folders[0]  # 返回找到的第一个匹配项
        else:
            sys.exit(f"{base_path}下未找到该文件夹: {pattern}")  # 如果没有找到匹配项，则退出

    def set_driver(self, url, browser):
        project_dir = os.path.abspath(os.path.join(self.common_dir, "utils"))
        driver_path = os.path.join(project_dir, 'driver')

        browser_options = {
            'chrome': (ChromeOptions, ChromeService, 'chromedriver', 'chromedriver'),
            'firefox': (FirefoxOptions, FirefoxService, 'geckodriver', 'geckodriver'),
            'edge': (EdgeOptions, EdgeService, 'edgedriver', 'msedgedriver')
        }

        if browser not in browser_options:
            sys.exit(f"不支持的浏览器: {browser}")

        options_class, service_class, driver_folder_name, driver_name = browser_options[browser]
        options = options_class()
        options.add_argument("--headless")  # Ensure GUI is off
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69'
        options.add_argument(user_agent)
        # 浏览器通用选项设置

        os_map = {
            'Linux': ('linux', ''),
            'Windows': ('win', '.exe'),
            'Mac': ('mac', '') 
        }

        current_os = self.get_os()
        if current_os not in os_map:
            sys.exit(f"不支持的操作系统: {current_os}")

        os_driver_folder_suffix, file_suffix = os_map[current_os]
        os_driver_folder =  self.regular_find_folder(driver_path, f'{driver_folder_name}*{os_driver_folder_suffix}*')
        driver_executable = f'{driver_name}{file_suffix}'
        driver_full_path = os.path.join(driver_path, os_driver_folder, driver_executable)

        service = service_class(executable_path=driver_full_path)

        driver = webdriver.Chrome(service=service, options=options) if browser == 'chrome' \
            else webdriver.Firefox(service=service, options=options) if browser == 'firefox' \
            else webdriver.Edge(service=service, options=options)

        driver.get(url)
        log.info(f'loading web page: {url}')
        return driver


 # 创建类的实例
wcgobj = WCGClass()

def wcgobj_method(method_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            method = getattr(wcgobj, method_name)
            return method(*args, **kwargs)
        return wrapper
    return decorator

@wcgobj_method('get_os')
def get_os():
    pass

@wcgobj_method('get_project_dir')
def get_project_dir(current_path):
    pass

@wcgobj_method('df2csv')
def df2csv(df, csv_name):
    pass

@wcgobj_method('regular_find_folder')
def regular_find_folder(base_path, pattern):
    pass

@wcgobj_method('set_driver')
def set_driver(url, browser):
    pass
