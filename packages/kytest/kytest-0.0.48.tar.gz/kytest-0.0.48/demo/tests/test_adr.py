from kytest import module, title
from kytest.adr import TestCase

from pages.adr_page import DemoPage


@module('测试demo')
class TestAdrDemo(TestCase):
    def start(self):
        self.dp = DemoPage(self.driver)

    @title('进入设置页')
    def test_go_setting(self):
        self.dp.adBtn.click_exists()
        self.dp.myTab.click()
        self.dp.setBtn.click()
        self.assert_act(self.dp.activity_name)
        self.screenshot("设置页")

    @title('进入全部服务')
    def test_all_service(self):
        self.dp.adBtn.click_exists()
        self.dp.moreService.click()
        self.screenshot('全部服务页')


