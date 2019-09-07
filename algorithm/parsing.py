from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
import json

config = None
with open("config.json",'r') as load_f:
    config = json.load(load_f)

# print(config)
cws_model_path = config['model']+'/cws.model'
pos_model_path = config['model']+'/pos.model'
par_model_path = config['model']+'/parser.model'
ner_model_path = config['model']+'/ner.model'

#初始化
segmentor = Segmentor()#分词
postagger = Postagger()#词性标注
recognizer = NamedEntityRecognizer()#命名主体识别
parser = Parser()#依存分析

segmentor.load(cws_model_path)
print('Segmentor Model Loaded')
postagger.load(pos_model_path)
print('Postagger Model Loaded')
recognizer.load(ner_model_path)
print('Recognizer Model Loaded')
parser.load(par_model_path)
print('Parser Model Loaded')

say_words = [':','诊断', '交代', '说', '说道', '指出','报道','报道说','称', '警告',
           '所说', '告诉', '声称', '表示', '时说', '地说', '却说', '问道', '写道', 
           '答道', '感叹', '谈到', '说出', '认为', '提到', '强调', '宣称', '表明', 
           '明确指出', '所言', '所述', '所称', '所指', '常说', '断言', '名言', '告知', 
           '询问', '知道', '得知', '质问', '问', '告诫', '坚称', '辩称', '否认', '还称', 
           '指责', '透露', '坦言', '表达', '中说', '中称', '他称', '地问', '地称', '地用',
           '地指', '脱口而出', '一脸', '直说', '说好', '反问', '责怪', '放过', '慨叹', '问起',
           '喊道', '写到', '如是说', '何况', '答', '叹道', '岂能', '感慨', '叹', '赞叹', '叹息',
           '自叹', '自言', '谈及', '谈起', '谈论', '特别强调', '提及', '坦白', '相信', '看来', 
           '觉得', '并不认为', '确信', '提过', '引用', '详细描述', '详述', '重申', '阐述', '阐释',
           '承认', '说明', '证实', '揭示', '自述', '直言', '深信', '断定', '获知', '知悉', '得悉', 
           '透漏', '追问', '明白', '知晓', '发觉', '察觉到', '察觉', '怒斥', '斥责', '痛斥', '指摘',
           '回答', '请问', '坚信', '一再强调', '矢口否认', '反指', '坦承', '指证', '供称', '驳斥', 
           '反驳', '指控', '澄清', '谴责', '批评', '抨击', '严厉批评', '诋毁', '责难', '忍不住', 
           '大骂', '痛骂', '问及', '阐明']

class Sentence:
    def __init__(self,sentence):
        self.words = segmentor.segment(sentence)
        self.postags = postagger.postag(self.words) #词性标注
        self.netags = recognizer.recognize(self.words, self.postags) #命名实体识别
        self.arcs = parser.parse(self.words, self.postags)  # 句法分析

    #命名实体识别
    def get_name_entity(self):
        # print(list(self.words))
        # print(list(self.netags))
        return self.netags

    # 句子依存分析
    def parsing(self):
        # print(' '.join("%d:%s" % (arc.head, arc.relation) for arc in self.arcs))
        return self.arcs

    def get_name(self):
        index = self.words.index()

    def get_posttags(self):
        return self.postags

    def get_words(self):
        return self.words

    def get_saying(self,start):
        pos = start
        while pos<len(self.words):
            relation = self.arcs[pos].relation
            # 谓语尚未结束
            if relation in ['DBL', 'CMP', 'RAD','VOP'] or self.words[pos]=='：':
                pos += 1
                continue
            head = self.arcs[pos].head
            # 定语
            if relation == 'ATT' :
                pos = head
                continue
            if self.words[pos] == '，':
                return ''.join(self.words[pos+1:])
            else:
                return ''.join(self.words[pos:])

    def get_subj(self,start):
        pos = start
        names = []
        while pos<len(self.words):
            if self.words[pos]=='，': break
            # 主语尚未结束
            relation = self.arcs[pos].relation
            if relation in ['LAD','ATT']:
                pos += 1
                continue
            head = self.arcs[pos].head
            # print(self.words[pos],relation)
            if relation in ['SBV','COO']:
                names.append(self.words[pos])
            pos += 1
        # print(names)
        return names

    def parse(self):
        names = None
        saying = ''
        entity = self.get_name_entity()
        wp = self.parsing()
        for k,v in enumerate(wp):
            # print(self.words[k],self.postags[k],v.relation,v.head)
            # print(self.words[v.head-1])
            if v.relation=='SBV' and (self.words[v.head-1] in say_words): #确定主谓句
                # name = self.words[k]
                names = self.get_subj(k)
                # print(names)
                if saying=='':
                    saying = self.get_saying(v.head)
                continue
        # print(names)
        return (names,saying)

