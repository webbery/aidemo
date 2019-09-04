from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SentenceSplitter

cws_model_path = '/home/webberg/ltp_data_v3.4.0/cws.model'
pos_model_path = '/home/webberg/ltp_data_v3.4.0/pos.model'
par_model_path = '/home/webberg/ltp_data_v3.4.0/parser.model'
ner_model_path = '/home/webberg/ltp_data_v3.4.0/ner.model'

#初始化
segmentor = Segmentor()#分词
postagger = Postagger()#词性标注
recognizer = NamedEntityRecognizer()#命名主体识别
parser = Parser()#依存分析

segmentor.load(cws_model_path)
postagger.load(pos_model_path)
recognizer.load(ner_model_path)
parser.load(par_model_path)

say_words = ['诊断', '交代', '说', '说道', '指出','报道','报道说','称', '警告',
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
            if relation in ['DBL', 'CMP', 'RAD','VOP']:
                pos += 1
                continue
            head = self.arcs[pos].head
            # 定语
            if head == 'ATT' :
                pos = head
                continue
            if self.words[pos] == '，':
                return ''.join(self.words[pos+1:])
            else:
                return ''.join(self.words[pos:])

    def parse(self):
        name = ''
        saying = ''
        entity = self.get_name_entity()
        wp = self.parsing()
        for k,v in enumerate(wp):
            # print(words[k],posttags[k],v.relation,v.head)
            if v.relation=='SBV' and (self.words[v.head-1] in say_words): #确定主谓句
                name = self.words[k]
                saying = self.get_saying(v.head)
                return (name,saying)
        return ('','')

#命名实体识别
def get_name_entity(sentence):
    #sentence = ''.join(strs)
    words = segmentor.segment(sentence)
    postags = postagger.postag(words) #词性标注
    netags = recognizer.recognize(words, postags) #命名实体识别
    print(list(netags))
    return netags

# 句子依存分析
def parsing(sentence):
    words = segmentor.segment(sentence)  # pyltp分词
    postags = postagger.postag(words)  # 词性标注
    arcs = parser.parse(words, postags)  # 句法分析
    print(' '.join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    return arcs

# 输入主语第一个词语、谓语、词语数组、词性数组，查找完整主语
def get_name( name, predic, words, property, ne):
    index = words.index(name)
    cut_property = property[index + 1:] #截取到name后第一个词语
    pre=words[:index]#前半部分
    pos=words[index+1:]#后半部分
    #向前拼接主语的定语
    while pre:
        w = pre.pop(-1)
        w_index = words.index(w)

        if property[w_index] == 'ADV': continue
        if property[w_index] in ['WP', 'ATT', 'SVB'] and (w not in ['，','。','、','）','（']):
            name = w + name
        else:
            pre = False

    while pos:
        w = pos.pop(0)
        p = cut_property.pop(0)
        if p in ['WP', 'LAD', 'COO', 'RAD'] and w != predic and (w not in ['，', '。', '、', '）', '（']):
            name = name + w # 向后拼接
        else: #中断拼接直接返回
            return name
    return name

# 获取谓语之后的言论
def get_saying(sentence, proper, heads, pos):
    # word = sentence.pop(0) #谓语
    if '：' in sentence:
        return ''.join(sentence[sentence.index('：')+1:])
    while pos < len(sentence):
        w = sentence[pos]
        p = proper[pos]
        h = heads[pos]
        # 谓语尚未结束
        if p in ['DBL', 'CMP', 'RAD']:
            pos += 1
            continue
        # 定语
        if p == 'ATT' and proper[h-1] != 'SBV':
            pos = h
            continue
        # 宾语
        if p == 'VOB':
            pos += 1
            continue
        # if p in ['ATT', 'VOB', 'DBL', 'CMP']:  # 遇到此性质代表谓语未结束，continue
        #    continue
        else:
            if w == '，':
                return ''.join(sentence[pos+1:])
            else:
                return ''.join(sentence[pos:])

def parse_sentence(sentence,  ws=False):
        #sentence = ' '.join([x for x in sentence.split('，') if x])
        print("sen", sentence)
        cuts = list(segmentor.segment(sentence))  # pyltp分词
        # 判断是否有‘说’相关词：
        #print(cuts)
        mixed = [word for word in cuts if word in say_words]
        #print("mixed  ",mixed)
        if not mixed : return False
        ne = get_name_entity(sentence) #命名实体
        wp = parsing(sentence) #依存分析
        wp_relation = [w.relation for w in wp]
        postags = list(postagger.postag(cuts))
        name = ''
        stack = [] 
        for k, v in enumerate(wp):
            # save the most recent Noun
            if postags[k] in ['nh', 'ni', 'ns']:
                stack.append(cuts[k])
            if v.relation=='SBV' and (cuts[v.head-1] in mixed) : #确定第一个主谓句
                name = get_name(cuts[k], cuts[v.head-1], cuts, wp_relation,ne)
                saying = get_saying(cuts, wp_relation, [i.head for i in wp], v.head)
                if not saying:
                    quotations = re.findall(r'“(.+?)”', sentence)
                    if quotations: says = quotations[-1]
                return name, saying
            # 若找到‘：’后面必定为言论。
            if cuts[k] == '：': 
                name = stack.pop()
                saying = ''.join(cuts[k+1:])
                return name, saying
        return False
    
# print(parse_sentence("今天很热，小王说明天不想去上班了。"))
# print(parse_sentence("小王说因为天气太热不想去上班了。他宣称这么热的天去上班可能会中暑。"))

# sentence = Sentence("今天很热，明天不想去上班了,小王说")
# sentence = Sentence("小王说因为天气太热不想去上班了。他宣称这么热的天去上班可能会中暑。")
# sentence = Sentence("今天很热，小王说明天不想去上班了。")
# print(sentence.parse())