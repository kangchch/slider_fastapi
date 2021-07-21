#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/9 16:33
# @Author  : Blackang
# @Email   : kcc813820@gmail.com
# @File    : jqka_slider.py
# @Software: vim

# import requests as rq
import time
import random
from extensions.custom_log import logger
import sys

sys.path.append('..')


ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 \
) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


class SpiderUrl(object):
    def __init__(self, browser, slider):
        self.slider = slider
        self.broswer = browser
        self.C = 2
        self.headers = {
            'User-Agent': ua
        }

    def spider_url(self, jurl):
        try:
            # res = rq.get(jurl, headers=self.headers)
            self.broswer.get(jurl)
            self.broswer.implicitly_wait(20)
            rdom = random.uniform(0, 0.6)
            sp = round(rdom, self.C)
            time.sleep(sp)
            res = self.broswer.page_source

            if 'sli-captcha' not in res:
                return {'result': res}
            else:
                page_source = self.slider.run(self.broswer, jurl)
                return {'result': page_source}
        except Exception as e:
            logger.error(f'get error: {jurl} - {str(e)}')
