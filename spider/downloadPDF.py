#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import logging
import random
from spider.verify_img_ocr import ocr
from spider.CONFIG import USER_NAME_LIST
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
download_dir = "D:\\project\\history_articles_download\\spider\\pdfs\\"

chrome_options.add_experimental_option('prefs', {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_dir, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
DRIVER = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"chromedriver.exe")
BASE_URL = "http://www.nssd.org"

UID = 0


def login(try_num = 5):
    global UID
    for try_i in range(try_num):
        try:
            logger.info("{} time(s) login ".format(try_i + 1))
            DRIVER.get("http://www.nssd.org/login.aspx")
            time.sleep(3)
            break
        except TimeoutException:
            time.sleep(60 * try_i + random.randint(30,60))
            logger.info("*********** {} timeout ***********".format(try_i+1))
            continue

    DRIVER.save_screenshot('pictures.png')  # 全屏截图
    img = DRIVER.find_element_by_id('verify_img')  # 验证码元素位置
    user_name = USER_NAME_LIST[UID]
    password = "ma123456"
    verify_img_str = ocr(img)
    DRIVER.find_element_by_id("txtuserName").send_keys(user_name)
    DRIVER.find_element_by_id("txtpassword").send_keys(password)
    DRIVER.find_element_by_id("verify_input").send_keys(verify_img_str)
    # 点击登录
    DRIVER.find_element_by_id("normalLogin").click()

def spider_pdf(url_links,try_num = 5):
    prefix = "http://www.nssd.org/articles/article_down.aspx?id="
    download_link = [prefix+ url.split("=")[1] for url in url_links]
    art_num = len(download_link)
    for di,du in enumerate(download_link):
        for try_i in range(try_num):
            try:
                DRIVER.get(du)
                time.sleep(random.randint(7,15))
                logger.info("try {} time(s) to download pdf {}".format(try_i + 1, du))
                break
            except TimeoutException:
                time.sleep(60 * try_i + random.randint(30, 60))
                logger.info("*********** {} timeout ***********".format(try_i))
                continue
            except Exception:
                logger.info("*********** Exception ***********")
                time.sleep(200)
                continue
        if di % 10 == 0:
            logger.info("-------------- {} / {} -----------".format(di+1,art_num))

if __name__ == "__main__":
    login()
    qkyearslist_url = pd.read_excel(r"../url/清史研究.xlsx")
    qkyearslist_url = qkyearslist_url.url.tolist()
    spider_pdf(qkyearslist_url)
    logger.info("Finish ! ")

