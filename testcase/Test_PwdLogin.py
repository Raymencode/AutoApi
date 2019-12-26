# -*- coding:utf-8 -*-
'''
Created on 2019-02-02
@author: Raymen
Project: 使用Pytest框架编写接口测试
'''

# 导入依赖模块
import pytest
import allure
import allure_report
import requests
import unittest
import json
# from pprint import pprint
# from requests.sessions import Session

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin



class TestUserPwdLogin():
    # def __init__(self, base_url):
    #     self.base_url = base_url
    # # 创建session实例
    #     self.session = Session()
    # @classmethod

    @pytest.fixture(scope="function",autouse=True)
    def pwdlogin(self):
        """
        详情接口
        """

        self.base_url = 'https://www.zhbbroker.com/yiiapp/user-pwd/user-pwd-login'
        self.mobile = '15921570877'
        self.pwd = '5c0c64d0caef1c81b913e0929d1ba52ea4b91d8794aa19b96bd7d8d33cbc09e5'
        self.version = '4.2.2'
        self.data = {
            'mobile': self.mobile,
            'pwd': self.pwd,
            'version': self.version
        }

        self.response_json = requests.post(url=self.base_url, data=self.data).json()
        rpheader = requests.post(url=self.base_url, data=self.data).headers
        print(self.response_json)
        print(rpheader)
        # rep = self.response
        return self.response_json

    @allure.step('返回码校验')
    def test_login_sucess(self):
        assert self.response_json['return_code'] == '0'
        print('登录成功')

if __name__ == '__main__':
    pytest.main()
