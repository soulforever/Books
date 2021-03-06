# -*- coding: utf-8 -*-

from math import sqrt

__author__ = 'guti'


critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0},
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5},
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0},
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5},
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0},
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5},
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0}
}


def sim_distance(prefs, person1, person2):
    """
    欧几里得距离评价
    :param prefs: 评分表
    :param person1: 评分表中人
    :param person2: 评分表中人
    :return: 0-1之间的数, 1表示偏好完全一样, 0表示不相关
    """
    # 相似表
    si = dict()

    # 获取有哪些是电影是person1和person2都有的
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 完全没有相似的电影
    if len(si) == 0:
        return 0

    # 书里这里没利用si表
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2) for item in si])

    # 分母+1是为了不会出现除0
    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    """
    皮尔逊相关系数
    :param prefs: 评分表
    :param p1: 评分表中人
    :param p2: 评分表中人
    :return: 相关系数为-1到1的数, 1表示完全相同的看法
    """
    # 获取两人共有的属性
    si = dict()
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # 记录共有属性长度
    n = len(si)
    if n == 0:
        return 0

    # 求和
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    # 求平方和
    sum1_sq = sum([pow(prefs[p1][item], 2) for item in si])
    sum2_sq = sum([pow(prefs[p2][item], 2) for item in si])

    # 求乘积和
    p_sum = sum([prefs[p1][item]*prefs[p2][item] for item in si])

    # 皮尔逊距离计算
    num = p_sum - (sum1 * sum2) / n
    den = sqrt((sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    """
    获取与用户A品味最相似的用户列表
    :param prefs: 评分表
    :param person: 待计算的用户
    :param n: 取n个最相似的其他用户
    :param similarity: 相似度计算方法,这里包括sim_pearson和sim_distance
    :return: 一个由元组(相似度, 其他用户)组成的列表,长度为n
    """
    # 计算一个用户和其他的相似度
    # 使用元组(相似度, 其他用户)存储
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    scores.sort()
    scores.reverse()

    # n为返回top n个与用户相似的其他用户
    return scores[:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    """
    为用户A推荐他没有看过的电影
    :param prefs: 评分表
    :param person: 待计算的用户
    :param similarity: 相似度计算方法,这里包括sim_pearson和sim_distance
    :return: 一个由元组(估算评分, 其他用户)组成的列表
    """
    # 评分权重总计表
    totals = dict()
    # 用户相似度总计表
    sim_sums = dict()
    for other in prefs:
        # 不计算与自身的相似度
        if other == person:
            continue

        # 用户间相似度值计算
        sim = similarity(prefs, person, other)

        # 相似度小于等于0忽略
        if sim <= 0:
            continue

        # 对每一部评分电影,计算评分权重总和,统计用户相似度和
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)

                # 评分权重 = 其他用户的评分 * 其他用户与该用户的相似度
                totals[item] += prefs[other][item] * sim

                # 相似度之和统计
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    # 排序,以元组(评分权重总和/相似度总和, 电影名称)存储
    rankings = [(total/sim_sums[item], item) for item, total in totals.iteritems()]
    rankings.sort(reverse=True)
    return rankings


def _transform_prefs(prefs):
    """
    帮助函数,用于转置评分表
    :param prefs: 原评分表
    :return: 一个转置后的评分表
    """
    result = dict()
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # 用户电影字典,转换为电影用户字典
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, n=10):
    """
    计算相似物品表,通过评分表转置,复用求最相似的top_matches函数
    :param prefs: 评分表
    :param n: 相似个数
    :return: n个最相似的物品,及其评分
    """
    # 相似物品表
    result = dict()
    # 对评分表转置把物品作为外层键
    item_prefs = _transform_prefs(prefs)

    c = 0
    for item in item_prefs:
        c += 1
        if c % 100 == 0:
            # 状态更新,类似进度条
            print '%d / %d' % (c, len(item_prefs))
        # 对转置后的表求出最相似的物品
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, item_match, user):
    """
    为指定用户推荐商品,使用相似物品表
    由于相似物品表只需要一次计算就可多次使用,这样的效率更高
    :param prefs: 相似表
    :param item_match: 使用calculate_similar_items计算出来的相似物品表
    :param user: 需要物品推荐服务的用户
    :return: 推荐排行表
    """
    # 某个用户的评分表
    user_rating = prefs[user]
    # 物品的带权重的用户评分
    scores = dict()
    # 物品的相似度总和
    total_sim = dict()

    for (item, rating) in user_rating.items():
        for (similarity, item2) in item_match[item]:

            # 用户评分过的不做计算
            if item2 in user_rating:
                continue

            # 用户没有评分的物品求加权和
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # 物品的相似度总和
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    # 合计加权和除以相似度总和的物品列表
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]
    rankings.sort(reverse=True)
    return rankings


def load_movielens(path='data/movielens'):
    """
    从网络下载的MovieLens数据集,然后使用该函数加载成为评分表.
    下载地址: "http://grouplens.org/datasets/movielens/"下十万条数据集.
    :param path: 数据集路径.
    :return: 电影评分表.
    """
    # 获取影片id到标题的映射关系
    movies = dict()
    with open(path + '/u.item') as f:
        for line in f:
            m_id, title = line.split('|')[:2]
            movies[m_id] = title
    # 生成影片评分表
    prefs = dict()
    with open(path + '/u.data') as f:
        for line in f:
            u_id, m_id, rating, ts = line.split('\t')
            prefs.setdefault(u_id, {})
            prefs[u_id][movies[m_id]] = float(rating)
    return prefs


if __name__ == '__main__':
    print 'Lisa Rose 与 Gene Seymour 的欧几里得距离评价'
    print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')

    print '\nLisa Rose 与 Gene Seymour 的皮尔逊相关系数'
    print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')

    print '\n与 Toby 最相似的3个人'
    print top_matches(critics, 'Toby', n=3)

    print '\n给 Toby 推荐电影,使用皮尔逊相关系数计算'
    print get_recommendations(critics, 'Toby')

    print '\n给 Toby 推荐电影,使用欧几里得距离评价计算'
    print get_recommendations(critics, 'Toby', similarity=sim_distance)

    print '\n通过用户们对各个电影的评分,计算 Superman Returns 最相近的电影列表'
    movies_critics = _transform_prefs(critics)
    print top_matches(movies_critics, 'Superman Returns')

    print '\n计算最相似的物品,使用欧几里得距离'
    item_sim = calculate_similar_items(critics)
    print item_sim

    print '\n给 Toby 的推荐电影,使用物品相似度表'
    print get_recommended_items(critics, item_sim, 'Toby')

    print '\n使用MovieLens数据集:'
    prefs_dict = load_movielens()
    print '\t依据相似用户给87用户的推荐电影'
    print get_recommendations(prefs_dict, '87')[:30]

    item_sim = calculate_similar_items(prefs_dict, n=50)
    print '\t使用相似物品表给87用户推荐电影'
    print get_recommended_items(prefs_dict, item_sim, '87')[:30]
