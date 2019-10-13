# import jieba
import math
import stanfordnlp
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDF:
    def __init__(self):
        # config = {
        #     'processors': 'tokenize',
        #     'models_dir': 'D:/UnixlikePrograms/nlp/stanford_resources',
        #     'lang':'zh'
        # }
        # self._nlp = stanfordnlp.Pipeline(**config)
        # self._tf = TfidfVectorizer()

    def vectorizer(self,news):
        doc = self._nlp(news)
        print(len(doc.sentences))
        self._sentences=[]
        for sent in doc.sentences:
            sentence=""
            for word in sent.words:
                sentence += word.text+" "
            self._sentences.append(sentence)
        # print(tokenize)
        data = self._tf.fit_transform(self._sentences)
        # tf-idf是如何得到特征的?
        # print("特征：")
        # print(tf.get_feature_names())
        # print("特征的大小：")
        # print(len(tf.get_feature_names()))
        # print("词向量：")
        # print(data.toarray())
        # print("第一列词向量的个数:")
        # print(len(data.toarray()[0]))
        return data.toarray()

    def display(self,indexes):
        for idx in range(len(indexes)):
            if indexes[idx]==True:
                print(self._sentences[idx])

