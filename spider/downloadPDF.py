#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from selenium.common.exceptions import TimeoutException
import logging
import random
import pymysql
from spider.login import manual_login

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = pymysql.connect("localhost", "root", "admin", "nssd")
cursor = db.cursor()

def spider_pdf(DRIVER,jornal_name,try_num = 5):
    prefix = "http://www.nssd.org/articles/article_down.aspx?id="
    # 获取需要下载的 url
    sql = "select url from history_geography where journal = '{}' and pdf is Null".format(jornal_name)
    cursor.execute(sql)
    results = cursor.fetchall()
    url_links = list(results)
    # url 转换
    download_link = [prefix+ url[0].split("=")[1] for url in url_links]
    art_num = len(download_link)
    logger.info("本次共需要下载 {} 篇论文".format(art_num))
    DRIVER.save_screenshot(r'./temp/pictures.png')  # 全屏截图
    success_download = []
    try:
        for di,du in enumerate(download_link):
            try:
                DRIVER.get(du)
                time.sleep(random.randint(10,15))
                logger.info("download pdf {} success".format( du))
                success_download.append(url_links[di][0])
            except TimeoutException:
                logger.info("*********** timeout ***********")
                time.sleep(random.randint(100, 150))
                continue
            except Exception:
                logger.info("*********** Exception ***********")
                continue
            finally:
                if di % 10== 0:
                    logger.info("-------------- {} / {} -----------".format(di + 1, art_num))
                    time.sleep(random.randint(60,120))
    finally:
        save_log(success_download,jornal_name)
        print("download seccess rate {:.2f}".format(len(success_download) / len(url_links)))
        logger.info("Finish !")

def save_log(success_download,jornal_name):
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
if __name__ == "__main__":
    DRIVER = manual_login()
    spider_pdf(DRIVER,"古代文明")

