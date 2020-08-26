# -*- coding: UTF-8 -*-

from lxml import etree

__author__ = 'lpe234'


class ParseArticle(object):
    """
    解析网页
    """

    def __init__(self, page_path):
        self.page_path = page_path

    def run(self):
        page_source = self.get_page_source()
        root = etree.HTML(page_source)
        comments = root.xpath('//div[@class="comment-list-box"]/div[contains(@class, "comment-list")]/div[@class="item"]')
        for comment in comments:
            username = self.fix_content(comment.xpath('.//div[@class="meta-box"]//span[@class="name"]/text()'))
            content = self.fix_content(comment.xpath('.//div[@class="content"]//text()'))
            print(f'{username} --> {content}')

    def get_page_source(self):
        """
        获取网页源码
        :return:
        """
        with open(self.page_path, 'r') as page:
            return ''.join(page.readlines())

    @staticmethod
    def fix_content(content):
        if isinstance(content, list):
            content = ''.join(content)
        content = content.strip()
        return content


if __name__ == '__main__':
    PAGE_PATH = './file/🏆 技术专题第三期 | 数据可视化的那些事 - 掘金.html'
    parse_article = ParseArticle(PAGE_PATH)
    parse_article.run()
