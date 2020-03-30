#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import logging
import random
import pymysql

from spider.verify_img_ocr import ocr
from spider.CONFIG import USER_NAME_LIST
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = pymysql.connect("localhost", "root", "admin", "nssd")
cursor = db.cursor()

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

UID = -1

def login(try_num = 5):
    global UID
    UID = (UID + 1) % len(USER_NAME_LIST)
    for try_i in range(try_num):
        DRIVER.delete_all_cookies()
        try:
            DRIVER.get("http://www.nssd.org/login.aspx")
            logger.info("login {} success".format(USER_NAME_LIST[UID]))
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

def spider_pdf(jornal_name,try_num = 5):
    prefix = "http://www.nssd.org/articles/article_down.aspx?id="
    # 获取需要下载的 url
    sql = "select url from history_geography where journal = '{}' and pdf <> 1".format(jornal_name)
    cursor.execute(sql)
    results = cursor.fetchall()
    url_links = list(results)
    # url 转换
    download_link = [prefix+ url.split("=")[1] for url in url_links]
    art_num = len(download_link)
    success_download = []
    try:
        for di,du in enumerate(download_link):
            for try_i in range(try_num):
                try:
                    DRIVER.get(du)
                    time.sleep(random.randint(5,10))
                    logger.info("download pdf {} success".format( du))
                    success_download.append(url_links[di])
                    break
                except TimeoutException:
                    time.sleep(60 * try_i + random.randint(30, 60))
                    logger.info("*********** {} timeout ***********".format(try_i))
                    if try_i == try_num-1:
                        logger.info("更换下载账号")
                        login()
                    continue
                except Exception:
                    logger.info("*********** fail ***********")
                    continue
            if di % 10 == 0:
                logger.info("-------------- {} / {} -----------".format(di+1,art_num))
    finally:
        # 保存已经成功下载过的论文，避免重复下载
        if len(success_download) >0:
            sql = "UPDATE history_geography set pdf = 1 WHERE url in ({})".format("','".join(success_download))
            cursor.execute(sql)
            db.commit()
            with open("success_download.log.txt","a","utf-8") as f:
                str_now = time.strftime('%Y-%m-%d %H:%M:%S')
                f.write("###### {} ###### \n".format(str_now))
                for url in success_download:
                    f.write("{} {}\n".format(jornal_name,url))
            print("download seccess rate {:.2f}".format(len(success_download)/len(url_links)))
        logger.info("Finish !")
if __name__ == "__main__":
    login()
    spider_pdf("古代文明")

