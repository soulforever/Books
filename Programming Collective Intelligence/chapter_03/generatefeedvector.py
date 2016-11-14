# -*- coding:utf-8 -*-

import feedparser
import re

__author__ = 'Guti'


def getwordcounts(url):
    """
    返回一个RSS订阅源标题和包含的单词计数字典.
    :param url: RSS订阅的URL地址.
    :return: 元组, 由题目和单词计数表构成.
    """
    data = feedparser.parse(url)
    word_count = dict()

    for e in data.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

        words = getwords(e.title + '' + summary)
        for word in words:
            word_count.setdefault(word, 0)
            word_count[word] += 1
    try:
        print url
        return data.feed.title, word_count
    except AttributeError:
        return None


def getwords(html):
    """
    获取一个html文档中的纯文本单词.
    :param html: html字符串表示.
    :return: 纯文本单词的列表.
    """
    # 去除html标记
    txt = re.compile(r'<[^>]+>').sub('', html)

    # 利用所有的非字母字符串拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # 转化为小写模式
    return [word.lower() for word in words if word != '']


def main():
    # 出现单词的博客数量
    apc_count = dict()
    # 每篇博客的单词计数
    word_counts = dict()
    feed_list = [line for line in file('feedlist.txt') if not line.startswith('#')]

    # 获取 单词-博客计数表 和 博客-单词 计数表
    print '订阅单词计数统计'
    for feed_url in feed_list:
        result = getwordcounts(feed_url)
        if result:
            title, word_count = result
        else:
            continue
        word_counts[title] = word_count
        for word, count in word_count.iteritems():
            apc_count.setdefault(word, 0)
            if count > 1:
                apc_count[word] += 1

    # 针对 博客-单词计数表, 选取词频范围
    print '词频过滤'
    word_list = list()
    for word, blog_count in apc_count.iteritems():
        frac = float(blog_count) / len(feed_list)
        if .1 < frac < .5:
            word_list.append(word)

    # 结果写入文件
    print '写入文件'
    with open('test_blogdata.txt', 'w') as out:
        out.write('BLOG')
        for word in word_list:
            out.write('\t%s' % word)
        out.write('\n')
        for blog, word_count in word_counts.iteritems():
            out.write(blog)
            for word in word_list:
                if word in word_count:
                    out.write('\t%s' % word_count[word])
                else:
                    out.write('\t0')
            out.write('\n')

if __name__ == '__main__':
    main()
