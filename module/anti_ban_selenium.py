# encoding=utf-8
# -*- coding:utf-8-*-
import logging
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options

DEFAULT_UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'


class AntiBan():

    """anti ban module by selenium"""

    def __init__(self, browser_type='chrome', use_proxy=False,
                 use_requests=False, ua=''):
        self.logger = logging.getLogger('anti_ban_selenium')
        self.use_proxy = use_proxy
        self.use_requests = use_requests
        self.ua = ua if ua else DEFAULT_UA
        self.browser_type = browser_type.lower()
        self.browser = None

    def __del__(self):
        pass

    def get_broswer(self):

        if self.browser_type == 'chrome':
            opts = Options()
            opts.add_argument('--headless')
            opts.add_argument('--disable-gpu')
            opts.add_argument('--no-sandbox')
            opts.add_argument('disable-infobars')
            opts.add_argument('--disable-dev-shm-usage')
            opts.add_argument('disable-browser-side-navigation')
            opts.add_argument("user-agent=%s" % (self.ua))
            opts.add_argument('--disable-blink-features=AutomationControlled')
            opts.add_experimental_option('useAutomationExtension', False)
            # prefs = {"profile.managed_default_content_settings.images":2}
            # opts.add_experimental_option("prefs",prefs)
            # window.navigator.webdriver
            opts.add_experimental_option(
                'excludeSwitches', ['enable-automation'])

            chrome_driver = "chromedriver"
            self.browser = webdriver.Chrome(chrome_driver, options=opts)
            self.browser.implicitly_wait(10)
            self.browser.set_page_load_timeout(10)
        else:
            pass

        self.wait = ui.WebDriverWait(self.browser, 120)
        self.logger.info('get %s broswer\nUA:%s\n requests:%s support',
                         self.browser_type, self.ua,
                         ' ' if self.use_requests else ' not ')
        return self.browser

    def browser_quit(self):
        try:
            if self.browser:
                self.browser.quit()
        except Exception as e:
            self.logger.warning("AntiBan - browser quit error:%s" % (str(e)))
        finally:
            self.browser = None


def test():
    at = AntiBan('chrome', False, False)
    broswer = at.get_broswer()
    broswer.get('https://www.ip.cn/ip/1.1.1.1.html')
    ele = broswer.find_element_by_xpath(
        "//tr[1]/th/div")
    ip = ele.text
    ele = broswer.find_element_by_xpath(
        "//div[@id='tab0_address']")
    local = ele.text
    print(ip, local)


if __name__ == '__main__':
    test()
