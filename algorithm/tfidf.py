import jieba
import math

class tfidf(docs):
    def __init__(self, docs):
        self.docs = docs
        self.word_count = len(doc)

    def tf(self, word):
        return len(word)/self.word_count

    def idf(self,word):
        # get document count which contain word
        doc_count_of_word = 0
        for doc in self.docs:
            if doc[word]>0: doc_count_of_word+=1
        return math.log(len(self.docs)/(doc_count_of_word+1))

    def score(self,word):
        return tf(self,word)*idf(self,word)
