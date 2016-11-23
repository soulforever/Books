# -*- coding:utf-8 -*-
"""
第三章练习题3和4, 使用不同的距离度量方法对博客和zebo数据集聚类.
从绘制的博客图像中可以总结:
    1.使用欧几里得距离度量的博客聚类效果很差,观察两篇和Google相关的blog.
    2.原因是即使是用词相似的文章,由于其词汇出现次数不同,其欧几里得距离仍会较大.
    3.改进的方法使用TF-IDF统计.
从绘制的zebo图像可以总结:
    1.使用曼哈顿聚聚里度量的zebo数据集效果也不好,观察car,house,money的位置.
    2.原因是这了的zebo数据集是由0,1构成,单词的词汇距离都是1.
"""

import math

__author__ = 'Guti'


def manhattan_distance(v1, v2):
    """
    曼哈顿距离实现.
    :param v1: 向量,使用列表表示.
    :param v2: 向量,使用列表表示.
    :return: 向量的曼哈顿距离.
    """
    return sum([abs(item1 - item2) for item1, item2 in zip(v1, v2)])


def euclidean_similarity(v1, v2):
    """
    欧几里得距离实现.
    :param v1: 向量,使用列表表示.
    :param v2: 向量,使用列表表示.
    :return: 介于0.0-1.0, 1.0表示完全相关, 0.0表示完全不相关.
    """
    sum_of_squares = sum([pow(item1-item2, 2) for item1, item2 in zip(v1, v2)])
    return 1 / (1 + math.sqrt(sum_of_squares))


if __name__ == '__main__':
    from clusters import readfile, hcluster, drawdendrogram

    print '绘制使用欧几里得距离的博客分级聚类结果:',
    blog_titles, words, vec_data = readfile('data/blogdata.txt')
    blog_clust_with_euclidean = hcluster(vec_data, distance=euclidean_similarity)
    drawdendrogram(blog_clust_with_euclidean, labels=blog_titles, jpeg='data/blogclust_euclidean.jpg')
    print '绘制完成,图像已存储.'

    print '绘制使用曼哈顿距离的博客分级聚类结果:',
    wants, people, wants_data = readfile('data/zebo.txt')
    zebo_clust_with_manhattan = hcluster(wants_data, distance=manhattan_distance)
    drawdendrogram(zebo_clust_with_manhattan, labels=wants, jpeg='data/zebowants_manhattan.jpg')
    print '绘制完成,图像已存储.'

    print '<完成>'
