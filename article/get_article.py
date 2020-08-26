# -*- coding: UTF-8 -*-

import os

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__author__ = 'lpe234'


class GetArticle(object):
    """
    获取网页源码
    """
    def __init__(self, article_url, store_path):
        self.driver = Chrome()
        self.article_url = article_url
        self.store_path = store_path

    def run(self):
        self.driver.get(self.article_url)
        # 等待评论列表出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'comment-list'))
        )
        self.save_page()

    def save_page(self):
        """
        保存网页源码
        :return:
        """
        filepath = os.path.join(self.store_path, self.driver.title + '.html')
        with open(filepath, 'w+') as pagefile:
            pagefile.write(self.driver.page_source)

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    # 文章地址
    ARTICLE_URL = 'https://juejin.im/post/6864072407461101582'
    # 数据存储地址
    STORE_PATH = './file'
    get_article = GetArticle(ARTICLE_URL, STORE_PATH)
    get_article.run()
