# -*- coding: utf-8 -*-

__author__ = 'guti'


def _items_in_both(prefs, person1, person2):
    """
    帮助函数，获取共有属性的列表
    """
    return [item for item in prefs[person1] if item in prefs[person2]]


def _square_and_dot(prefs, person1, person2, si):
    """
    帮助函数，获取共有属性的列表
    :param prefs: 评分表
    :param person1: 评分表中人
    :param person2: 评分表中人
    :param si: 共有属性列表
    :return: 元组(平方和， 平方和， 点积)
    """
    # 求平方和
    sum1_sq = sum([pow(prefs[person1][item], 2) for item in si])
    sum2_sq = sum([pow(prefs[person2][item], 2) for item in si])

    # 求乘积和
    p_sum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    return sum1_sq, sum2_sq, p_sum


def sim_tanimoto(prefs, person1, person2):
    """
    谷本相关系数计算
    """
    # 相似列表
    si = _items_in_both(prefs, person1, person2)

    # 完全没有相似的电影
    if len(si) == 0:
        return 0

    sum1_sq, sum2_sq, p_sum = _square_and_dot(prefs, person1, person2, si)

    return p_sum / (sum1_sq + sum2_sq - p_sum)


def sim_cosine(prefs, person1, person2):
    """
    余弦相似度计算
    """
    # 相似列表
    si = _items_in_both(prefs, person1, person2)

    # 完全没有相似的电影
    if len(si) == 0:
        return 0

    sum1_sq, sum2_sq, p_sum = _square_and_dot(prefs, person1, person2, si)

    return p_sum / sum1_sq + sum2_sq


if __name__ == '__main__':
    from recommendations import critics, get_recommendations, sim_pearson

    print 'Lisa Rose 与 Gene Seymour 的谷本(Tanimoto)系数评价'
    print sim_tanimoto(critics, 'Lisa Rose', 'Gene Seymour')

    print '\n给 Toby 推荐电影，使用皮尔逊相关系数计算'
    print get_recommendations(critics, 'Toby', similarity=sim_pearson)

    print '\n给 Toby 推荐电影，使用谷本相似度评价计算'
    print get_recommendations(critics, 'Toby', similarity=sim_tanimoto)

    print '\n给 Toby 推荐电影，使用余弦相似度评价计算'
    print get_recommendations(critics, 'Toby', similarity=sim_cosine)
