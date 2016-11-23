# -*- coding:utf-8 -*- 

"""
第二章习题3,预先用户相似度,当需要用户相似度参数的时候直接查表即可.

方法:
    类似书中基于物品过滤的方法建表,只是不需要再转置评分表.
"""

from recommendations import top_matches, sim_pearson

__author__ = 'Guti'


def calculate_similar_users(prefs, n=5):
    """
    计算相似用户表,不需要转置评分表
    :param prefs: 评分表
    :param n: 相似用户表中存储的相似用户个数
    :return: 相似用户表
    """
    # 相似用户表
    result = dict()

    c = 0
    for user in prefs:
        c += 1
        if c % 100 == 0:
            # 进度条状态更新
            print '%d / %d' % (c, len(prefs))
        # 求出该用户与其他用户的相似表
        scores = top_matches(prefs, user, n=n, similarity=sim_pearson)
        result[user] = scores
    return result


if __name__ == '__main__':
    from recommendations import critics

    print '打印预先计算的相似用户表'
    print calculate_similar_users(critics)['Toby']
