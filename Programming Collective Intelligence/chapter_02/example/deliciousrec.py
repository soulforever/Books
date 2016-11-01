# -*- coding: utf-8 -*-

import time

from helpers.pydelicious import get_popular, get_userposts, get_urlposts, \
    PyDeliciousException, DeliciousError

__author__ = 'guti'


def initialize_user_dict(tag, count=5):
    """
    获取最近提交的热门链接中提交过的用户
    :param tag: 标签类别
    :param count: 需要获取的数量，默认为5
    :return: 用户字典，类似评分表
    """
    user_dict = dict()

    # 获取当前最受欢迎的张贴记录
    for p1 in get_popular(tag=tag)[:count]:
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict[user] = dict()
    return user_dict


def fill_items(user_dict):
    all_items = dict()

    # 查找所有用户提交过的连接
    for user in user_dict:
        posts = None
        # 尝试3次，每次间隔4秒
        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except (PyDeliciousException, DeliciousError):
                print 'Failed user' + user + ', retrying...'
                time.sleep(4)
        if posts is not None:
            for post in posts:
                url = post['href']
                user_dict[user][url] = 1.0
                all_items[url] = 1
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0


if __name__ == '__main__':
    delusers = initialize_user_dict('programming')
    delusers['tsegaran'] = dict()
    import pickle
    fill_items(delusers)
    pickle.dumps(delusers)
