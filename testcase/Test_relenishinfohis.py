# -*- coding:utf-8 -*-
'''
Created on 2018-07-04
@author: Raymen
Project: 使用Pytest框架编写接口测试
'''

# 导入依赖模块
import pytest
import requests
import allure_report
from pprint import pprint
from requests.sessions import Session

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class InstanceAPI(object):
    def __init__(self, base_url):
        self.base_url = base_url
    # 创建session实例
        self.session = Session()

    def replenishinfohistory(self):
        """
        详情接口
        """
        #self.base_url = 'https://www.zhbbroker.com/yiiapp/'
        url = urljoin(self.base_url, 'car-info/replenish-info-history')
        #payload = {'version': '3.6.0'}
        #self.rq = requests.get(url=url)
        response = self.session.get(url=url)
        print('\n*****************************************')
        print(u'\n1、请求url: \n%s' % url)
        print(u'\n2、请求头信息:')
        pprint(self.session.headers)
        print(u'\n3、请求cookies:')
        pprint(dict(self.session.cookies))
        print(u'\n4、响应:')
        pprint(response.json())
        return response


# 定义测试类
class TestRih():
    # 初始化
    @pytest.fixture(scope="function",autouse=True)
    def setup_class(cls):
        cls.base_url = 'https://www.zhbbroker.com/yiiapp/'
        cls.app = InstanceAPI(cls.base_url)
        cls.response = cls.app.replenishinfohistory()

    @pytest.allure.step('验证服务器状态码返回')
    def test_statuscode(self):
        # 验证服务器状态
        assert self.response.status_code == 200

    @pytest.allure.step('第一辆车的车牌号')
    def test_ftcar_license(self):
        # 验证第一个车牌号是否正确
        assert self.response.json()["data"][0]["license_no"] == "渝ACV350"

    @pytest.allure.step('日期不为空')
    def test_ftcar_lastime_isnotNUll(self):
        # 验证第一个车牌号是否正确
        assert self.response.json()["data"][0]["last_replenish_time"] != ''

    @pytest.allure.step('列表最大车辆数')
    def test_carcount(self):
        #验证获取的历史车辆列表最大数
        self.count = 0
        for num in range(20):
            vin = self.response.json()["data"][num]["frame_no"]
            if vin != '':
                print(vin)
                self.count += 1
            else:
                print("no car")
                break
        assert self.count == 11



if __name__ == "__main__":
    pytest.main()