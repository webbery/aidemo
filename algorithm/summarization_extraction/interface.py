import pandas as pd
import numpy as np
import jieba
import os
from AutoSummarization import Summarization
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