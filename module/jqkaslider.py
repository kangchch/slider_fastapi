#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/9 16:33
# @Author  : Blackang
# @Email   : kcc813820@gmail.com
# @File    : jqka_slider.py
# @Software: vim

import cv2
import time
import random
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from extensions.custom_log import logger
import sys
import os

sys.path.append('..')


class CrackSlider():
    def __init__(self, jqka_pic_path):
        self.jqka_pic_path = jqka_pic_path
        current_dir = (
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        ttr_pic_path = os.path.join(current_dir, self.jqka_pic_path)
        if not os.path.exists(ttr_pic_path):
            os.makedirs(ttr_pic_path)

        self.targetjpg = os.path.join(ttr_pic_path, 'target.jpg')
        self.templatepng = os.path.join(ttr_pic_path, 'template.png')
        self.resultpng = os.path.join(ttr_pic_path, 'result.png')

    def is_exists(self, ):
        pass

    def get_img(self, browser, wait, target, template, xp):
        time.sleep(1)
        target_link = wait.until(EC.presence_of_element_located(
            (By.ID, 'slicaptcha-img'))).get_attribute('src')
        time.sleep(1)
        template_link = browser.find_element_by_xpath(
            "//*[@id='slicaptcha-block']").get_attribute('src')
        time.sleep(1)
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save(target)
        template_img.save(template)
        # 按比例缩放
        size_loc = target_img.size
        zoom = xp / int(size_loc[0])
        return zoom

    @staticmethod
    def clear_white(img):
        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imread(img)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y: max_y]
        return img1

    def template_match(self, tpl, target):
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0,0,255)：矩形边框颜色
        # 2：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        cv2.imwrite(self.resultpng, target)
        return tl[0]

    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def discern(self, bg, gap):
        img1 = self.clear_white(gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        back = cv2.imread(bg, 0)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = self.template_match(slide_pic, back_pic)
        return x

    def slide_track(self, distance, seconds, ease_func):
        distance += 35
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = ease_func
            offset = round(ease(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        tracks.extend([-2, -2, -2, -2, -1, -2, -1, -1, -0, -1, -1])
        return tracks

    def slide_to_gap(self, browser, wait, tracks):
        slider = wait.until(EC.element_to_be_clickable((By.ID, 'slider')))
        ActionChains(browser).click_and_hold(slider).perform()
        while tracks:
            x = tracks.pop(0)
            ActionChains(browser).move_by_offset(
                xoffset=x, yoffset=0).perform()
            time.sleep(0.05)
        time.sleep(0.05)
        ActionChains(browser).release().perform()

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def run(self, browser, jurl):
        browser.get(jurl)
        current_url = browser.current_url
        logger.info(f'slider url: {current_url}')
        wait = WebDriverWait(browser, 20)
        xp = 320
        self.get_img(browser, wait, self.targetjpg, self.templatepng, xp)
        distance = self.discern(self.targetjpg, self.templatepng)
        if distance <= 0:
            self.run(browser, jurl)
        track = self.slide_track(
            distance, random.randint(2, 4), self.ease_out_quart)
        self.slide_to_gap(browser, wait, track)
        time.sleep(1)

        try:
            failure = browser.find_element_by_xpath(
                "//span[@id='slicaptcha-text']")
        except Exception:
            logger.info('hey boy, you dead')
            page_source = browser.page_source
            # browser.close()
            return page_source
        time.sleep(1)
        if failure.text == u'向右拖动滑块填充拼图':
            logger.info('hey boy, you win, next crack slide')
            return self.run(browser, jurl)
