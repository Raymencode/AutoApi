# -*- coding:utf-8 -*-
'''
Created on 2019-02-02
@author: Raymen
Project: 使用Pytest框架编写接口测试
'''

# 导入依赖模块
import pytest
import requests
import allure
import allure_report
from pprint import pprint
from requests.sessions import Session

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class Login_Pwd(object):
    def login_pwd(self):
        url = "https://zhbbroker.com/yiiapp/user-pwd/user-pwd-login"
        payload = {'mobile': '15921570877',
                   'pwd': 'fdbc6f40e9e178dd990058bb52888552342a35bb7ed0ca547c9a67eeb2dbb5b6', 'login_type': '17',
                   'source_type': 'wechat'}

        # headers = {
        #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        #     'cache-control': "no-cache",
        #     'postman-token': "487c0231-0871-470a-20b4-b2f6aa05a3eb"
        #     }
        r = requests.post(url=url, data=payload)
        zhbcookie = (r.headers['Set-Cookie'].split(';')[0])
        return zhbcookie

class InstanceAPI(object):
    def __init__(self, base_url):
        self.base_url = base_url
    # 创建session实例
        self.session = Session()


    def lately_search_car(self):
        """
        详情接口
        """
        self.temp_session = Login_Pwd.login_pwd(self)
        print(self.temp_session)
        #self.base_url = 'https://www.zhbbroker.com/yiiapp/'
        url = urljoin(self.base_url, 'home-config/lately-more-search-car')
        #payload = {'version': '3.6.0'}
        temp = 'pgv_pvi=1282623488; pgv_si=s5447865344; user_id=692808; PHPSESSID=6f7v19iunn2cb5kt8600eua9u2; Hm_lvt_79ee0e9f63d4bd87c861f98a6d497993=1561447079; Hm_lpvt_79ee0e9f63d4bd87c861f98a6d497993=1561909903;'+str(self.temp_session)
        print(temp)
        headers = {'Cookie':temp}
        response = self.session.get(url=url,headers=headers)
        # 'user_id':'692808', 'ZHBSESSID':'880705d5e8ae98-a73b-468b-a2b3-68ed18b89e4c'
        print('\n*****************************************')
        print(u'\n1、请求url: \n%s' % url)
        print(u'\n2、请求头信息:')
        pprint(self.session.headers)
        print(u'\n3、请求cookies:')
        pprint(dict(self.session.cookies))
        print(u'\n4、响应:')
        pprint(response.json()['data'])
        return response


# 定义测试类
class Test_LatelySearchCar():
    # 初始化
    # @classmethod
    #@pytest.fixture(scope="function",autouse=True)
    def setup_class(cls):
        cls.base_url = 'https://www.zhbbroker.com/yiiapp/'
        cls.app = InstanceAPI(cls.base_url)
        cls.response = cls.app.lately_search_car()
        print(cls.response)

    @allure.step('验证服务器状态码返回')
    def test_statuscode(self):
        # 验证服务器状态
        assert self.response.status_code == 200

    @allure.step('第一辆车的车架号')
    def test_ftcar_license(self):
        # 验证第一个车牌号是否正确
        assert self.response.json()["data"][0]["frame_no"] == "LBECFAHB2HZ520602"

    @allure.step('日期不为空')
    def test_ftcar_lastime_isnotnull(self):
        # 验证第一个车牌号是否正确
        assert self.response.json()["data"][0]["last_replenish_time"] != ''

    @allure.step('列表最大车辆数')
    def test_carcount(self):
        #验证获取的历史车辆列表最大数
        self.count = 0
        for num in range(14):
            vin = self.response.json()["data"][num]["frame_no"]
            if vin != '':
                print(vin)
                self.count += 1
            else:
                print("no car")
                break
        assert self.count == 14



if __name__ == "__main__":
    pytest.main()
