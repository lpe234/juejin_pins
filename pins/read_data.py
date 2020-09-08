# -*- coding: UTF-8 -*-

import json
import logging
import time
import os

import pymysql

__author__ = 'lpe234'


class Pins(object):
    """
    沸点
    """
    msg_id = None
    topic_id = None
    topic_title = None
    user_id = None
    user_name = None
    msg_content = None
    msg_ctime = None
    msg_digg_count = 0      # 点赞数
    msg_comment_count = 0   # 评论数

    def parse_from_item(self, item: dict):
        self.msg_id = item['msg_id']
        self.topic_id = item['topic']['topic_id']
        self.topic_title = item['topic']['title']
        self.user_id = item['author_user_info']['user_id']
        self.user_name = item['author_user_info']['user_name']
        self.msg_content = item['msg_Info']['content']
        self.msg_ctime = item['msg_Info']['ctime']
        self.msg_digg_count = item['msg_Info']['digg_count']
        self.msg_comment_count = item['msg_Info']['comment_count']
        return self

    def __repr__(self):
        return '<Pins: %s>' % self.msg_id


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s', )


conn = pymysql.Connect(
    host='127.0.0.1',
    database='juejin',
    user='root',
    password='root',
    port=3306,
)

cursor = conn.cursor()


def insert_db(items: list):
    sql = 'INSERT INTO juejin.pins' \
          '(msg_id, topic_id, topic_title, user_id, user_name, msg_content, msg_ctime, msg_digg_count, ' \
          'msg_comment_count, msg_createdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    items_params = []
    for item in items:
        items_params.append((item.msg_id, item.topic_id, item.topic_title, item.user_id, item.user_name,
                             item.msg_content, item.msg_ctime, str(item.msg_digg_count), str(item.msg_comment_count),
                             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item.msg_ctime)))))
    try:
        cursor.executemany(sql, items_params)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        logging.warning(ex)


def read_all_data():
    """
    遍历读取所有json数据，然后入库
    :return:
    """
    pins_list = []
    for dirpath, dirnames, filenames in os.walk('./json_data'):
        filenames = sorted(filenames, key=lambda _: _[5: 9])
        for filename in filenames:
            filename = os.path.join('./json_data', filename)
            print(filename)
            with open(filename, 'r') as pins_file:
                items_data = json.loads(''.join(pins_file.readlines()))['data']
                for item in items_data:
                    pins = Pins().parse_from_item(item)
                    pins_list.append(pins)
                    insert_db([pins])
    return pins_list


if __name__ == '__main__':
    read_all_data()

