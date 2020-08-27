# -*- coding: UTF-8 -*-

import os
import time
import logging

import requests


__author__ = 'lpe234'


sess = requests.Session()
sess.headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://juejin.im',
    'pragma': 'no-cache',
    'referer': 'https://juejin.im/pins/hot',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}

# 沸点URL
HOT_URL = 'https://apinew.juejin.im/recommend_api/v1/short_msg/hot'
# 数据保存地址
DATA_PATH = 'json_data'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s', )


def save_pins(idx=0, cursor='0'):
    """
    存储沸点数据
    :param idx: 索引
    :param cursor: 游标指针
    :return:
    """
    json_data = {
        'id_type': 4,
        'sort_type': 200,
        'cursor': cursor,
        'limit': 200
    }
    resp = sess.post(HOT_URL, json=json_data)
    if resp.ok:
        resp_json = resp.json()
        with open(f'{DATA_PATH}/pins-{idx:04}.json', 'w+') as json_file:
            json_file.write(resp.content.decode('UTF-8'))
        # 是否还有更多
        if resp_json['err_no'] == 0 and resp_json['err_msg'] == 'success':
            logging.debug(f'no error, idx={idx}')
            if resp_json['has_more']:
                logging.debug(f'has more, next idx={idx+1}')
                time.sleep(5)
                save_pins(idx+1, cursor=resp_json['cursor'])
        else:
            # 出了异常
            logging.warning(resp_json['err_msg'])
            logging.debug(f'sleep 10s, retry idx={idx}')
            time.sleep(10)
            save_pins(idx, cursor)


def check_path():
    """
    校验data_path
    :return:
    """
    logging.debug('check data_path')
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH, mode=0o744)


if __name__ == '__main__':
    check_path()
    save_pins()
