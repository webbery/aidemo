import json

config = None
with open("./config.json",'r') as load_f:
    config = json.load(load_f)
print(config)

from collections import defaultdict
import pandas as pd
from gensim.models import Word2Vec
from sklearn.decomposition import TruncatedSVD
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
model = Word2Vec.load(config['wordvec']+"/wiki.model")
word_vectors = model.wv
del model
print('load word model finished')
feature_size=32
#思路:
# 寻找跟整个文章相关性高的句子
# 在拿到句子后，(寻找跟句子相关性高的词
# 将词拼成句子，)然后将句子拼成摘要
class Summarization:
    def __init__(self,doc):
        
        # 切分句子和单词
        sentences,sentences_with_punctuation = cs.cut_and_segment([doc],doc_type='pandas',segment_type='array')

        self.sentences = pd.DataFrame({'word':sentences,'sentence':sentences_with_punctuation})
        self.p_w,self.total_words_count =get_tf(self.sentences['word'])
        self.document = doc
        # 生成句向量
        self.vectors = self.get_sentence_embedding_via_sif(self.sentences)

    def split_sentence(self,sentence):
        pass

    # 尝试采用SIF sentence embedding
    def get_sentence_embedding_via_sif(self,sentences):
        alpha = 0.001
        # sentence_vectors = []
        sentence_vec=np.zeros((len(sentences),feature_size))
        for idx,row in sentences.iterrows():
            # print('sentence: ',row['word'])
            for word in row['word']:
                if word in word_vectors.vocab:
                    sentence_vec[idx] += word_vectors[word]*(alpha/(alpha+self.p_w[word]/self.total_words_count))

        svd = TruncatedSVD(n_components=1,n_iter=5,random_state=0)
        svd.fit(sentence_vec)
        pc = svd.components_
        #计算每个句子的句向量
        embeds = sentence_vec-sentence_vec.dot(pc.transpose()) * pc
        # print(embed.shape)
        return embeds

    def get_corrlations_with_document(self):
        #切分整个文本，变成词向量
        content = cs.segment(self.document)
        words = pd.DataFrame({'word':[content]})
        embed = self.get_sentence_embedding_via_sif(words)
        correlations=[]
        for sentence in self.vectors:
            correlations += [cosine(embed,sentence)]
        self.sentences['cor']=correlations
        return correlations

    def get_summarization(self):
        #取跟整个文本相关性大于1的句子
        self.get_corrlations_with_document()
        indexes = self.sentences['cor']>1
        #构造句子图
        prob = likely_probability(self.vectors)
        sentence_graph = nx.Graph()
        for idx, item in enumerate(indexes):
            # print(idx,item)
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
        # print('================')
        sentences = tops.sort_index()
        # plt.plot(sentences['score'])
        # plt.show()
        # print(sentences)
        # 句子组装成摘要
        abstract=''
        for sentence in sentences['sentence']:
            abstract += sentence
        return abstract
