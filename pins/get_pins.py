# -*- coding: UTF-8 -*-

import requests

__author__ = 'lpe234'


HOT_URL = 'https://apinew.juejin.im/recommend_api/v1/short_msg/hot'


def main():
    json_form = {
        'cursor': '0',
        'id_type': 4,
        'limit': 20,
        'sort_type': 200,
    }
    resp = requests.post(HOT_URL, json=json_form)
    print(resp.json())


if __name__ == '__main__':
    main()
