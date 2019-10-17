import pandas as pd
import numpy as np
import jieba
import os
from algorithm.summarization_extraction.AutoSummarization import Summarization
import networkx as nx
import matplotlib.pyplot as plt

# def cut(string): return ' '.join(jieba.cut(string))
# path_root = '.'
# news_file = os.path.join(path_root, 'sqlResult_1558435.csv') 
# news_content = pd.read_csv(news_file, encoding='gb18030')
# contents = news_content['content'].dropna(axis=0, how='any')

def get_abstract(content):
    summarization = Summarization(content)
    return summarization.get_summarization()

#print(get_abstract('俄罗斯对意大利应美国要求拘留俄罗斯公民感到愤怒。”美国司法部5日宣称，57岁的俄罗斯“间谍”科尔舒诺夫和59岁的意大利“间谍”比安齐因涉嫌窃取美国通用电气航空集团商业机密在意大利那不勒斯机场被拘留。对此，俄罗斯总统普京及俄外交部对意大利此举表示强烈不满，并警告称这种行为是不公平竞争的一个例子，将损害两国关系。'))
