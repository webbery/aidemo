# import stanfordnlp
# from stanfordcorenlp import StanfordCoreNLP
import pagerank
import numpy as np
from parsing import Sentence
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# stanfordnlp.download('zh',resource_dir='D:/UnixlikePrograms/nlp/stanford_resources')
# nlp = stanfordnlp.Pipeline(lang='zh',models_dir='D:/UnixlikePrograms/nlp/stanford_resources',processors="tokenize,lemma,pos,depparse")
text = """
但韩国网友对“韩国海军陆战队世界第二”的说法不以为然。不少网友留言嘲讽称：“这似乎是韩国海军陆战队争取国防预算的软文”。
"""
# doc = nlp(text)
# doc.sentences[0].print_dependencies()
# print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')

def process_news(news):
    #split sentences
    pattern = re.compile('.+?[。！]')
    sentences = pattern.findall(news)
    print(sentences)
    results = []
    for sentence in sentences:
        sent = Sentence(sentence)
        result = sent.parse()
        results.append(result)
    # print(sentences)
    # tfidf = TfidfVectorizer()
    # model = tfidf.fit(sentences)
    # sparse_matrix = model.transform(sentences)
    # m = pagerank.likely_probability(sparse_matrix)
    # pagerank.PR_score(m)
    return results

process_news(text)
# 
# vec = tf_idf.vectorizer(text)
# m = pagerank.likely_probability(vec)
# pagerank.score(m)
# PR = pagerank.PR_score(m).reshape(1,-1)[0]
# max_num_index=np.argpartition(PR,3)
# print(max_num_index<=2)
# tf_idf.display(max_num_index<=2)
# nlp = StanfordCoreNLP('D:/UnixlikePrograms/nlp/stanford_resources/')