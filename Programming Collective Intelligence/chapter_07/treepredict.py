# -*- coding:utf-8 -*- 

from math import log

__author__ = 'Guti'

my_data = [['slashdot', 'USA', 'yes', 18, 'None'],
           ['google', 'France', 'yes', 23, 'Premium'],
           ['digg', 'USA', 'yes', 24, 'Basic'],
           ['kiwitobes', 'France', 'yes', 23, 'Basic'],
           ['google', 'UK', 'no', 21, 'Premium'],
           ['(direct)', 'New Zealand', 'no', 12, 'None'],
           ['(direct)', 'UK', 'no', 21, 'Basic'],
           ['google', 'USA', 'no', 24, 'Premium'],
           ['slashdot', 'France', 'yes', 19, 'None'],
           ['digg', 'USA', 'no', 18, 'None'],
           ['google', 'UK', 'no', 18, 'None'],
           ['kiwitobes', 'UK', 'no', 19, 'None'],
           ['digg', 'New Zealand', 'yes', 12, 'Basic'],
           ['slashdot', 'UK', 'no', 21, 'None'],
           ['google', 'UK', 'yes', 18, 'Basic'],
           ['kiwitobes', 'France', 'yes', 19, 'Basic']]


class DecisionNode(object):
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        # 列索引
        self.col = col
        # 决策树判断的临界值
        self.value = value
        # 节点为叶子节点时的结果,非叶子节点为None
        self.results = results
        # 子树节点
        self.tb = tb
        self.fb = fb


def divide_set(rows, column, value):
    """
    在某一列上对数据集拆分,能够处理数值型和名词型.
    :param rows: list, 二维数据表.
    :param column: int, 用于数据分离的列.
    :param value: 如果是int和float, 为分离的临界点.
    :return: tuple, 由两个表示拆分结果的list构成.
    """
    # 定义不通类型值的分离函数.
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda r: r[column] >= value
    else:
        split_function = lambda r: r[column] == value

    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]

    return set1, set2


def unique_counts(rows):
    """
    统计所有不同的可能结果.
    :param rows: list, 二维数据表.
    :return: dict, key: 可能结果, value: 出现频次.
    """
    results = dict()
    for row in rows:
        # 计数的是最后一列的结果
        r = row[-1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


def gini_impurity(rows):
    """
    当数据项随机放置的时候错误分类的概率.
    :param rows: list,需要计算预期误差率的数据.
    :return: float, 基尼不纯度.0表示所有结果相同.
    """
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp


def entropy(rows):
    """
    熵值的计算,即所有可能的p(x)log(p(x))的和.
    :param rows: list, 需要计算误差率的数据.
    :return: float,熵值.0表示所有结果相同.
    """
    log2 = lambda x: log(x) / log(2)
    total = len(rows)
    counts = unique_counts(rows)

    ent = .0
    for k in counts:
        p = float(counts[k]) / total
        ent -= p * log2(p)
    return ent


def build_tree(rows, score=entropy):
    """
    建立决策树.通过计算寻找每个属性的信息最大增益,决定用来拆分的属性.
    :param rows: list, 二维数据表.
    :param score: function, 用于衡量结果差异的测度函数.
    :return: DecisionNode, 决策树.
    """
    if len(rows) == 0:
        return DecisionNode()
    current_score = score(rows)

    # 最佳拆分条件的记录
    best_gain = .0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(column_count):
        # 当前列不同值构成的序列
        column_values = dict()
        for row in rows:
            column_values[row[col]] = 1
        # 尝试该列中的每一个值,对数据做拆分
        for value in column_values:
            set1, set2 = divide_set(rows, col, value)

            p = float(len(set1)) / len(rows)
            gain = current_score - p * score(set1) - (1-p) * score(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = col, value
                best_sets = set1, set2

    # 递归创建子树
    if best_gain > 0:
        true_branch = build_tree(best_sets[0])
        false_branch = build_tree(best_sets[1])
        return DecisionNode(col=best_criteria[0], value=best_criteria[1], tb=true_branch, fb=false_branch)
    else:
        return DecisionNode(results=unique_counts(rows))


def print_tree(tree, indent=''):
    """
    打印决策树辅助函数.
    :param tree: DecisionNode, 决策树根节点.
    :param indent: str, 缩进.
    :return: None.
    """
    # 判断是否为叶子节点
    if tree.results is not None:
        print str(tree.results)
    else:
        print str(tree.col) + ':' + str(tree.value) + '? '
        print indent + 'T->',
        print_tree(tree.tb, indent+'  ')
        print indent + 'F->',
        print_tree(tree.fb, indent+'  ')


if __name__ == '__main__':
    # test
    divide_result = divide_set(my_data, 2, 'yes')
    divide_set1, divide_set2 = divide_result

    # print 'True', '\tFalse'
    # for true_part, false_part in zip(*divide_result):
    #     print true_part[-1], false_part[-1]

    # print gini_impurity(my_data), entropy(my_data)
    # print gini_impurity(divide_set1), entropy(divide_set2)

    decision_tree = build_tree(rows=my_data)
    print_tree(decision_tree)
