# -*- coding:utf-8 -*-

from math import sqrt
from PIL import Image, ImageDraw

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


def get_height(clust):
    """
    获取二叉树表示的分级聚类结果的高度和.
    :param clust: 二叉树的根节点.
    :return: 树高和.
    """
    # 叶子节点的高度为一
    if clust.left is None and clust.right is None:
        return 1
    # 分支节点的高度等于左右树的和
    else:
        return get_height(clust.left) + get_height(clust.right)


def get_depth(clust):
    """
    节点误差深度,即所属每个分支的最大误差.
    :param clust: 二叉树根节点.
    :return: 误差和.
    """
    # 叶子节点的距离是0.0
    if clust.left is None and clust.right is None:
        return 0
    # 分支节点的距离等于左右分支距离较大者,加分支节点自身的距离
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    """
    创建绘图板,每个聚类占20像素.调整根节点位置到中心.
    :param clust: 二叉树根节点.
    :param labels: 标签的列表,用于展示.
    :param jpeg: 图片路径和名称.
    :return: None.
    """
    # 图像高度和宽度
    height = get_height(clust) * 20
    width = 1200
    depth = get_depth(clust)

    # 单位误差深度所占的像素
    scaling = float(width - 150) / depth

    # 新建画板
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, height/2, 10, height/2), fill=(255, 0, 0))

    draw_node(draw, clust, 10, height/2, scaling, labels)
    img.save(jpeg, 'JPEG')


def draw_node(draw, clust, x, y, scaling, labels):
    """
    绘制每一个聚类节点, 包括聚类的指示线.
    :param draw: 绘图板引用.
    :param clust: 二叉树根节点.
    :param x: 绘图起始x座标.
    :param y: 绘图起始y座标.
    :param scaling: 缩放值,即单位误差锁占像素.
    :param labels: 标签的列表,用于展示.
    :return: None.
    """
    if clust.id < 0:
        # 如果是分支节点
        height_1 = get_height(clust.left) * 20
        height_2 = get_height(clust.right) * 20

        top = y - (height_1 + height_2) / 2
        bottom = y + (height_1 + height_2) / 2

        # 线长,由单位误差所占的像素 乘以 节点的误差
        line_len = clust.distance * scaling

        # 到子类的垂直线
        draw.line((x, top+height_1/2, x, bottom-height_2/2), fill=(255, 0, 0))

        # 连接左侧节点
        draw.line((x, top+height_1/2, x+line_len, top+height_1/2),fill=(255, 0, 0))

        # 连接右侧节点
        draw.line((x, bottom-height_2/2, x+line_len, bottom-height_2/2), fill=(255, 0, 0))

        # 画左右子树
        draw_node(draw, clust.left, x+line_len, top+height_1/2, scaling, labels)
        draw_node(draw, clust.right, x+line_len, bottom-height_2/2, scaling, labels)
    else:
        # 否则是叶子节点,直接打印标签
        draw.text((x+5, y-7), labels[clust.id], (0, 0, 0))


def rotate_matrix(data):
    """
    数据集转置,该例中用来分析数据集:每个单词再不同文章中出现的次数.
    实际场景中,可以分析类似那些产品可以捆绑销售.
    :param data: 待转置的数据集.
    :return: 转置后的数据集.
    """
    new_data = list()
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data


if __name__ == '__main__':
    blog_titles, words, vec_data = readfile('blogdata.txt')
    blog_clust = hcluster(vec_data)
    print '打印分级聚类到命令行:'
    print_clust(blog_clust, labels=blog_titles)

    print '绘制分级聚类图像:'
    drawdendrogram(blog_clust, blog_titles, jpeg='blogclust.jpg')

    print '绘制单词的分级聚类:'
    rotate_data = rotate_matrix(vec_data)
    word_clust = hcluster(rotate_data)
    drawdendrogram(word_clust, words, jpeg='wordclust.jpg')
    print '<结束>'