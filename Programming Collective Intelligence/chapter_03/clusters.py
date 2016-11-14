# -*- coding:utf-8 -*- 

__author__ = 'Guti'


def readfile(filename):
    """
    从文件中读取数据,格式为第一行列名,第一列行名,其他表格位置为数据
    可以参考blogdata.txt
    :param filename: 文件路径
    :return: 元组,由行名列表,列名列表,数据构成
    """

    with open(filename) as f:
        lines = (line for line in f)

        # 第一行为标题
        col_names = lines[0].strip.split('\t')[1:]
        row_names = list()
        data = list()

        for line in lines[1:]:
            p = line.strip().split('\t')
            # 每一行第一列是行名
            row_names.append(p[0])
            # 剩余部分是数据
            data.append([float(x) for x in p[1:]])
        return row_names, col_names, data
