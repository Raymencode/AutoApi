#!/usr/bin/python
# coding=utf-8

import unittest
import pytest
import requests

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

#
# class TestalienTest:
#
#     @classmethod
#     def setUpClass(cls):
#         print("TestCase  start running ")
#
#     def test_1_run(self):
#         print("hello world_1")
#
#     def test_2_run(self):
#         print("hello world_2")
#
#     def test_3_run(self):
#         print("hello world_3")
#
# if __name__ == '__main__':
#     print("hello world")
#     pytest.main()
#!/usr/bin/python
# coding=utf-8


class DemoApi(object):
    def __init__(self, base_url):
        self.base_url = base_url
    def login(self, username, password):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        """
        url = urljoin(self.base_url, 'login')
        data = {
            'username': username,
            'password': password
        }
        return requests.post(url, data=data).json()
    def get_cookies(self, username, password):
        """
        获取登录cookies
        """
        url = urljoin(self.base_url, 'login')
        data = {
            'username': username,
            'password': password
        }
        return requests.post(url, data=data).cookies
    def info(self, cookies):
        """
        详情接口
        """
        url = urljoin(self.base_url, 'info')
        return requests.get(url, cookies=cookies).json()

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://127.0.0.1:5000'
        cls.username = 'admin'
        cls.password = '123456'
        cls.app = DemoApi(cls.base_url)
    def test_login(self):
        """
        测试登录
        """
        response = self.app.login(self.username, self.password)
        assert response['code'] == 200
        assert response['msg'] == 'success'
    # def test_info(self):
    #     """
    #     测试获取详情信息
    #     """
    #     cookies = self.app.get_cookies(self.username, self.password)
    #     response = self.app.info(cookies)
    #     assert response['code'] == 200
    #     assert response['msg'] == 'success'
    #     assert response['data'] == 'info'


if __name__ == '__main__':
    print("hello world")
    pytest.main()