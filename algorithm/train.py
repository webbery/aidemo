# import stanfordnlp
# from stanfordcorenlp import StanfordCoreNLP
import pagerank
import numpy as np
import parsing
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# stanfordnlp.download('zh',resource_dir='D:/UnixlikePrograms/nlp/stanford_resources')
# nlp = stanfordnlp.Pipeline(lang='zh',models_dir='D:/UnixlikePrograms/nlp/stanford_resources',processors="tokenize,lemma,pos,depparse")
text = """
新华社北京7月26日电国家主席习近平26日就突尼斯总统埃塞卜西不幸逝世向突尼斯代总统纳赛尔致唁电。
习近平代表中国政府和中国人民并以个人的名义，对埃塞卜西总统逝世表示深切的哀悼，向埃塞卜西总统亲属和突尼斯人民表示诚挚的慰问。
习近平表示，埃塞卜西总统是突尼斯杰出政治家。
他领导突尼斯人民努力克服国家发展遇到的各种挑战，为促进国家稳定和发展作出了积极努力。
埃塞卜西总统生前致力于促进中突关系发展，为推动两国友好合作、增进两国人民友谊作出了积极贡献。
中方高度重视中突关系发展，愿同突方携手努力，推动两国友好合作关系不断向前迈进。
同日，国务院总理李克强就埃塞卜西不幸逝世向突尼斯总理沙赫德致唁电，向突尼斯政府表示沉痛的哀悼，向埃塞卜西总统亲属表示诚挚的慰问。
"""
# doc = nlp(text)
# doc.sentences[0].print_dependencies()
# print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')

def process_news(news):
    #split sentences
    pattern = re.compile('.+[。！]')
    sentences = pattern.findall(news)
    print(sentences)
    tfidf = TfidfVectorizer()
    model = tfidf.fit(sentences)
    sparse_matrix = model.transform(sentences)

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