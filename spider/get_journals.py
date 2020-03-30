#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import logging
import pymysql
from multiprocessing import Process

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

driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r"chromedriver.exe")
# driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
base_url = "http://www.nssd.org"

def get_html(url,retry_num = 5):
    for i in range(retry_num):
        try:
            time.sleep(150*i+15)
            driver.get(url)
            tree = etree.HTML(driver.page_source)
            return tree
        except TimeoutException:
            pass
    return None


def fetch_article_download_url(qkyearslist_url,process_name):
    def get_issue(issue_url,issue_name,journal_name):
        logger.info("{} 开始爬取 {} - {} ".format(process_name,journal_name, issue_name))
        issue_html = get_html(base_url + issue_url)
        if not (issue_html is None):
            detail_urls = issue_html.xpath(
                '/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr/td[1]/a/@href')

            titles = issue_html.xpath(
                "/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr/td[1]//text()")

            return [[base_url+detail_url,titles[di],journal_name,issue_name] for di,detail_url in enumerate(detail_urls)]
        else:
            return None
    def insert_to_db():
        if len(res) > 0:
            cursor.executemany(r"INSERT INTO history_geography(url, title, journal, issue) VALUES (%s,%s,%s,%s)",
                               res)
            db.commit()
            logger.info("{} add {} records to db".format(process_name,len(res)))
            res.clear()

    res = [] # 爬取的结果
    un_crawler_list = [] # 没有能够成功爬取的网页
    try:
        for j,url in enumerate(qkyearslist_url):
            try:
                html = get_html(url)
                if html is None:
                    time.sleep(200)
                    un_crawler_list.append(url)
                    logger.info("{} fail".format(url))
                else:
                    journal_name = html.xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/h1/text()")[0]
                    issue_urls = html.xpath('//*[@id="numlist"]/ul/li//@href')
                    issue_names = html.xpath('//*[@id="numlist"]/ul/li//text()')
                    for i, issue_url in enumerate(issue_urls):
                        temp_res = get_issue(issue_url,issue_names[i],journal_name)
                        if temp_res is None:
                            time.sleep(100)
                            un_crawler_list.append(base_url+issue_url)
                            logger.info("{} fail".format(issue_url))
                        else:
                            res.extend(temp_res)
                if j % 5 == 0:
                    insert_to_db()
                    driver.delete_all_cookies() # 清除cookie
            except Exception:
                continue
    # 结果保存
    finally:
        un_crawler_df = pd.DataFrame(un_crawler_list,columns=["url"])
        un_crawler_df.to_excel("un_crawler_{}.xlsx".format(process_name),index = False)
        logger.info("{} finish !".format(process_name))


if __name__ == "__main__":
    qkyearslist_url = pd.read_excel(r"../url/article_2.xlsx")
    qkyearslist_url = qkyearslist_url.issue_link.tolist()
    preocess_num = 5 # 进程数
    ll = []
    part_len = len(qkyearslist_url)
    for i in range(preocess_num):
        temp = qkyearslist_url[i * int(part_len / preocess_num):(i + 1) * int(part_len / preocess_num) if i != preocess_num - 1 else part_len]
        p = Process(target=fetch_article_download_url,args=(temp,"process {}".format(i+1)))
        p.start()
        ll.append(p)
    for p in ll:
        p.join()
    logger.info("Finish ! ")

