"""
@Author: kang.yang
@Date: 2023/10/26 09:48
"""
import time
import json
import os

import allure
from urllib import parse

from .driver import WebDriver
from .element import WebElem
from kytest.api.request import HttpReq
from kytest.utils.log import logger
from kytest.utils.config import KyConfig


class TestCase(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: WebDriver = None

    # ---------------------初始化-------------------------------
    @classmethod
    def start_class(cls):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    @classmethod
    def end_class(cls):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        browserName = KyConfig.get_web("browser_name")
        headless = KyConfig.get_web("headless")
        maximized = KyConfig.get_web("maximized")
        window_size = KyConfig.get_web("window_size")

        state_file = KyConfig.get_web("state_file")
        if not state_file:
            try:
                cookies = KyConfig.get_web("cookies")
                if not os.path.exists("data"):
                    os.makedirs("data")
                state_file = os.path.join("data", "state.json")
                state_json = {
                    "cookies": cookies
                }
                if cookies:
                    with open(state_file, "w") as f:
                        f.write(json.dumps(state_json))
            except Exception as e:
                print(e)
                state_file = None

        cls.driver = WebDriver(
            browserName=browserName,
            headless=headless,
            state=state_file,
            maximized=maximized,
            window_size=window_size
        )
        cls.context = cls.driver.context
        cls.page = cls.driver.page
        cls.response_list = []

        # 处理响应事件
        def handle_response(response):
            # 把所有请求的响应都存入response_list
            try:
                res_json = response.json()
            except:
                res_json = {}
            logger.debug({
                'url': response.request.url,
                'param': response.request.post_data,
                'response': res_json
            })
            cls.response_list.append({
                'url': response.request.url,
                'param': response.request.post_data,
                'response': res_json
            })

        # cls.page.on('response', handle_response)  # 监控页面请求响应

        cls.start_class()

    @classmethod
    def teardown_class(cls):
        cls.end_class()
        cls.driver.close()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        project_name = KyConfig.get_common('project')
        if project_name:
            allure.dynamic.feature(project_name)
        self.start_time = time.time()
        self.start()

    def teardown_method(self):
        self.end()
        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

    # UI方法
    def elem(self, *args, **kwargs):
        return WebElem(self.driver, *args, **kwargs)

    # web方法
    def assert_title(self, title: str, timeout: int = 5):
        """断言页面标题"""
        self.driver.assert_title(title, timeout)

    @staticmethod
    def is_url_has_http(url):
        """针对为空和只有路径的情况，使用默认host进行补全"""
        host = KyConfig.get_common("web_base_url")
        if url is None:
            url = host
        if 'http' not in url:
            url = parse.urljoin(host, url)
        return url

    def assert_url(self, url: str = None, timeout: int = 5):
        """断言页面url"""
        url = self.is_url_has_http(url)
        self.driver.assert_url(url, timeout)

    def open(self, url):
        """打开页面"""
        url = self.is_url_has_http(url)
        self.driver.open(url)
        # cookies = config.get_web("cookies")
        # if cookies:
        #     self.driver.set_cookies(cookies)

