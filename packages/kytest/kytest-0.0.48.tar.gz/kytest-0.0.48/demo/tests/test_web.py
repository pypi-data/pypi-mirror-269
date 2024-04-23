"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
from kytest import module, title
from kytest.web import TestCase

from pages.web_page import LoginUtil


@module('登录模块')
class TestWebDemo(TestCase):

    def start(self):
        self.lu = LoginUtil(self.driver)

    @title("登录")
    def test_login(self):
        self.lu.login()
        self.assert_url()
        self.sleep(3)
        self.screenshot(self.index_name)



