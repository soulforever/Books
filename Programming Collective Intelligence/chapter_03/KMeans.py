# -*- coding:utf-8 -*-
"""
第三章练习题5和6,修改了KMeans聚类,一并返回所有数据项的距离总和以及各自中心点.
选用不同的k值查看聚类总距离随k的变化.
可以看出,一开始簇的增加会使聚类效果更好,到9个簇的时候趋势逐渐衰弱.
"""

from clusters import pearson, readfile
import random

__author__ = 'Guti'


def kmeans_cluster_improve(rows, distance=pearson, k=4):
    """
    k均值聚类实现,一并返回数据项的彼此距离总和和各自中心点.
    :param rows: 聚类的数据表.
    :param distance: 评价紧密度的函数.
    :param k: 簇的个数.
    :return: 一个长为k的列表,每一行代表该簇所包含的节点.
    """
    # 数据集没一列的范围
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]

    # 随机创建K个中心点
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                for i in range(len(rows[0]))] for _ in range(k)]

    last_matches = best_matches = None
    for t in range(100):
        print 'Iteration %d' % t
        best_matches = [list() for _ in range(k)]

        # 每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row):
                    best_match = i
            # 对数据集中每一行归类到相应的簇
            best_matches[best_match].append(j)

        # 如果上次计算结果与这一次相同,过程结束
        if best_matches == last_matches:
            break
        last_matches = best_matches

        # 中心点位置更新
        for i in range(k):
            averages = [.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for row_id in best_matches[i]:
                    for m in range(len(rows[row_id])):
                        averages[m] += rows[row_id][m]
                for j in range(len(averages)):
                    averages[j] /= len(best_matches[i])
                clusters[i] = averages

    # 距中心点的距离总和
    sum_distance = sum([distance(clusters[i], rows[best_matches[i][j]]) for i in range(k)
                        for j in range(len(best_matches[i]))])
    return sum_distance, clusters, best_matches


def different_k(data_path, k_stop=12):
    """
    模拟不同的k对距离总和的影响.
    :param data_path: 数据的路径.
    :param k_stop: 模拟的k的范围.
    :return: 不同k值的列表.
    """
    result = list()
    row_names, col_names, vec_data = readfile(data_path)
    for k in range(2, k_stop):
        k_clust_tuple = kmeans_cluster_improve(vec_data, k=k)
        result.append((k, k_clust_tuple[0]))
    return result


if __name__ == '__main__':
    k_changes = different_k('data/blogdata.txt')
    print k_changes
