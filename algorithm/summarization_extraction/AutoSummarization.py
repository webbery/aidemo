from collections import defaultdict
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.decomposition import TruncatedSVD
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# import cut_sentence as cs
import algorithm.summarization_extraction.cut_sentence as cs
import networkx as nx
import matplotlib.pyplot as plt

def likely_probability(vec_arr):
    n = len(vec_arr)
    m = np.zeros((n, n))
    # i->j的相似程度,等价于pagerank中i页面到j页面的转化概率
    for i in range(n):
        for j in range(i + 1, n):
            m[i, j] = cosine_similarity(vec_arr[i].reshape(1, -1),
                                        vec_arr[j].reshape(1, -1))[0][0]
            m[j, i] = m[i, j]
    return m

def get_tf(sentences):
    tf=defaultdict(int)
    total_words=0
    for sentence in sentences:
        for word in sentence:
            if not tf.__contains__(word):
                total_words+=1
            tf[word] += 1
        return tf,total_words

# 加载词向量
# model = Word2Vec.load(config['wordvec']+"/wiki.model")
# word_vectors = model.wv
# del model
# print('load word model finished')
from bert_serving.client import BertClient
bert = BertClient()

feature_size=32
#思路:
# 寻找跟整个文章相关性高的句子
# 在拿到句子后，(寻找跟句子相关性高的词
# 将词拼成句子，)然后将句子拼成摘要
class Summarization:
    def __init__(self,doc):
        # 切分句子和单词
        sentences,sentences_with_punctuation = cs.cut_and_segment([doc],doc_type='pandas',segment_type='array')
        # print(len(sentences))
        if len(sentences)<5:
            raise Exception('document to short')
        new_sentences = []
        new_puntuation = []
        # 剔除短句子（在新闻中短句子意义不大）
        for idx in range(len(sentences)):
            if len(sentences[idx])<=4: continue
            new_sentences.append(sentences[idx])
            new_puntuation.append(sentences_with_punctuation[idx])
        self.sentences = pd.DataFrame({'word':new_sentences,'sentence':new_puntuation})
        self.p_w,self.total_words_count =get_tf(self.sentences['word'])
        self.document = doc
        # 生成句向量
        alldocs=[]
        count = 0
        for line in new_sentences:
            # print(line)
            alldocs.append(line)
            count +=1
        self.vectors = bert.encode(alldocs,is_tokenized=True)
        # print(self.vectors.shape)

    def split_sentence(self,sentence):
        pass

    def get_corrlations_with_document(self):
        #切分整个文本，变成词向量
        content = cs.segment(self.document,type='arr')
        # print(len(content))
        doc = bert.encode([content],is_tokenized=True).flatten()
#        doc.train([content],total_examples=1,epochs=100)
        correlations=[]
        try:
            for sentence in self.vectors:
                correlations += [cosine(doc,sentence.flatten())]
            #correlations += [cosine(embed,sentence)]
        except:
            print('except')
        self.sentences['cor']=correlations
        # print(correlations)
        return correlations

    def get_summarize_of_sentence(self,sentence):
        pass

    def get_summarization(self):
        #取跟整个文本相关性高的句子
        cor = self.get_corrlations_with_document()
        cor.sort(reverse=True)
        # print(cor,cor[len(cor)//2])
        indexes = self.sentences['cor']>=cor[len(cor)//2+1]
        #构造句子图
        prob = likely_probability(self.vectors)
        sentence_graph = nx.Graph()
        for idx, item in enumerate(indexes):
            for t in range(len(indexes)):
                if item==True and indexes[t]==True and t!=idx:
                    # print('prob: ',prob[idx][t])
                    sentence_graph.add_edge(idx, t, weight=prob[idx][t])
        
        scores = nx.pagerank(sentence_graph,tol=10)

        scores_list = []
        for idx in range(len(indexes)):
            if not scores.__contains__(idx):
                scores_list.append(None)
            else:
                scores_list.append(scores[idx])
        # print(scores_list)
        # print('scores: ',len(scores_list))
        self.sentences['score']=scores_list
        sentences = self.sentences.dropna(axis=0,how='any')
        tops = sentences.sort_values(by=['score'],ascending=False)[:50]
        # 得到句子级摘要
        sentences = tops.sort_index()
        # 尝试对句子提取主要信息
        # print(sentences)
        # 句子组装成摘要
        abstract=''
        for sentence in sentences['sentence']:
            abstract += sentence
        return abstract
