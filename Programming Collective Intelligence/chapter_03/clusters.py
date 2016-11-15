# -*- coding:utf-8 -*-

from math import sqrt

__author__ = 'Guti'


def readfile(filename):
    """
    从文件中读取数据,格式为第一行列名,第一列行名,其他表格位置为数据
    可以参考blogdata.txt
    :param filename: 文件路径
    :return: 元组,由行名列表,列名列表,数据构成
    """

    with open(filename) as f:
        lines = [line for line in f]

        # 第一行为标题
        col_names = lines[0].strip().split('\t')[1:]
        row_names = list()
        data = list()

        for line in lines[1:]:
            p = line.strip().split('\t')
            # 每一行第一列是行名
            row_names.append(p[0])
            # 剩余部分是数据
            data.append([float(x) for x in p[1:]])
        return row_names, col_names, data


def pearson(v1, v2):
    """
    皮尔逊评价系数计算,用来定义聚类中的紧密度.
    使用皮尔逊评价的原因:
        皮尔逊系数计算的是两个向量对一条直线的拟合,排除了向量模的影响.
        不同的文章的词汇量不同,所以模长不一定相同.
    :param v1: 向量,使用列表表示.
    :param v2: 向量,使用列表表示.
    :return: 当完全匹配返回1.0, 完全不相关返回0.0
    """
    # 向量分量和
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 向量分量平方和
    sum1_sq = sum([pow(v, 2) for v in v1])
    sum2_sq = sum([pow(v, 2) for v in v2])

    # 向量内积
    p_sum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # 计算r,即皮尔逊评价
    length = float(len(v1))
    num = p_sum - (sum1 * sum2) / length
    den = sqrt((sum1_sq - pow(sum1, 2) / length) * (sum2_sq - pow(sum2, 2) / length))

    return 1.0 - num / den


class BICluster(object):
    """
    二叉树的节点类,最后形成的二叉树用于表示聚类结果.
    该对象的实例记录了:
        向量,左子节点,右子节点,距离,id
    """
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


def hcluster(rows, distance=pearson):
    """
    分级聚类实现.
    通过将最小距离配对聚类后缩小聚类列表,最后形成一个由二叉树表示的分级结果.
    :param rows: 聚类的数据表.
    :param distance: 评价紧密度的函数.
    :return: 二叉树的根节点.
    """
    # 聚类中各个向量的距离记录
    distances = dict()
    # 当前聚类簇的id
    current_clust_id = -1

    # 待聚类的实例列表,实例中的向量为读取数据的行,标志为其行号
    clust = [BICluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        # 配对初始化为第0,第1个配对
        lowest_pair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # 遍历所有配对,寻找最小距离的配对
        # 采用了第一次计算所有配对的距离,之后直接查询
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowest_pair = (i, j)

        # 由最小距离配对生成的新的向量
        merge_vec = [(clust[lowest_pair[0]].vec[i] + clust[lowest_pair[1]].vec[i]) / 2.0
                     for i in range(len(clust[0].vec))]

        # 生成新的聚类节点
        new_cluster = BICluster(merge_vec, left=clust[lowest_pair[0]],
                                right=clust[lowest_pair[1]],
                                distance=closest, id=current_clust_id)

        # 所有分支节点的标志为负数,分支节点其实是计算的中间量,没有实际意义
        current_clust_id -= 1
        # 注意: 这里不能使用直接删除的方式,由于要删除配对,所以索引会变化
        # 改进的方法是记录配对对应的值,然后删除
        clust = [x for x in clust if x != clust[lowest_pair[0]] and x != clust[lowest_pair[1]]]
        clust.append(new_cluster)
    return clust[0]


def print_clust(clust, labels=None, n=0):
    """
    打印二叉树表示的分级聚类结果.
    :param clust: 二叉树的根节点.
    :param labels: 标签列表,节点的展示方式.
    :param n: 层数的初始值,用于缩进.
    :return: None.
    """
    # 使用空格缩进展示层
    for i in range(n):
        print ' ',
    if clust.id < 0:
        # 负数表示为分支节点
        print '-'
    else:
        # 整数表示为叶子节点
        if labels is None:
            print clust.id
        else:
            print labels[clust.id]

    # 先左后右打印左右侧分支
    if clust.left is not None:
        print_clust(clust.left, labels=labels, n=n+1)
    if clust.right is not None:
        print_clust(clust.right, labels=labels, n=n+1)


if __name__ == '__main__':
    blog_titles, words, vec_data = readfile('blogdata.txt')
    clust_result = hcluster(vec_data)
    print_clust(clust_result, labels=blog_titles)
