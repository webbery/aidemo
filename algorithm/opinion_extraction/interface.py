from algorithm.opinion_extraction.parsing import Sentence
#from parsing import Sentence
import re

text = """
对此，俄罗斯总统普京及俄外交部对意大利此举表示强烈不满，并警告称这种行为是不公平竞争的一个例子，将损害两国关系。
"""
def process_news(news):
    #split sentences
    pattern = re.compile('.+?[。！]')
    sentences = pattern.findall(news)
    # print(sentences)
    results = []
    for sentence in sentences:
        sent = Sentence(sentence)
        result = sent.parse()
        if result[0]==None: continue
        results.append(result)
    if len(sentences)==0:
        sent = Sentence(news)
        result = sent.parse()
        results.append(result)
    return results

#print(process_news(text))
