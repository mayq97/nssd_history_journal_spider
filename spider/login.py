#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from spider.verify_img_ocr import ocr
from spider.CONFIG import USER_NAME_LIST

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
UID = 0


def get_DRIVER():
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
    return DRIVER



def manual_login(try_num = 5):
    global UID
    DRIVER = get_DRIVER()
    UID = (UID + 1) % len(USER_NAME_LIST)
    for try_i in range(try_num):
        DRIVER.delete_all_cookies()
        try:
            DRIVER.get("http://www.nssd.org/login.aspx")
            time.sleep(3)

            DRIVER.save_screenshot(r'./temp/pictures.png')  # 全屏截图
            user_name = USER_NAME_LIST[UID]
            password = "ma123456"
            code = input("验证码：")
            DRIVER.find_element_by_id("txtuserName").send_keys(user_name)
            DRIVER.find_element_by_id("txtpassword").send_keys(password)
            DRIVER.find_element_by_id("verify_input").send_keys(code)
            # 点击登录
            DRIVER.find_element_by_id("normalLogin").click()
            logger.info("login {} success".format(USER_NAME_LIST[UID]))
            time.sleep(random.randint(3, 6))
            return DRIVER
        except TimeoutException:
            time.sleep(60 * try_i + random.randint(30, 60))
            logger.info("*********** {} timeout ***********".format(try_i + 1))
            continue


def autom_login(try_num = 5):
    global UID
    DRIVER = get_DRIVER()
    UID = (UID + 1) % len(USER_NAME_LIST)
    for try_i in range(try_num):
        DRIVER.delete_all_cookies()
        try:
            DRIVER.get("http://www.nssd.org/login.aspx")
            time.sleep(3)
            break
        except TimeoutException:
            time.sleep(60 * try_i + random.randint(30,60))
            logger.info("*********** {} timeout ***********".format(try_i+1))
            continue

    for i in range(20):
        DRIVER.save_screenshot(r'./temp/pictures.png')  # 全屏截图
        img = DRIVER.find_element_by_id('verify_img')  # 验证码元素位置
        code = ocr(img)
        print("code:{}".format(code))
        if len(code) >= 4:
            user_name = USER_NAME_LIST[UID]
            password = "ma123456"
            DRIVER.find_element_by_id("txtuserName").send_keys(user_name)
            DRIVER.find_element_by_id("txtpassword").send_keys(password)
            DRIVER.find_element_by_id("verify_input").send_keys(code)
            # 点击登录
            DRIVER.find_element_by_id("normalLogin").click()
            time.sleep(random.randint(3,6))
            try:
                dig_alert = DRIVER.switch_to.alert
                alert = dig_alert.text
                dig_alert.accept()
                print(alert)
                if "验证码错误" in alert:
                    time.sleep(3)
                    continue
                elif "用户名" in  alert:
                    UID = (UID + 1) % len(USER_NAME_LIST)
            except Exception:
                logger.info("login {} success".format(USER_NAME_LIST[UID]))
                return DRIVER
        else:
            DRIVER.find_element_by_xpath("//*[@id='form1']/table/tbody/tr[3]/td[2]/a").click()
        return False
