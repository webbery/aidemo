from lxml import etree
# import networkx as nx
# import matplotlib.pyplot as plt
import json
import math

class DomTree():
    def __init__(self):
        self.name_idx = 1
        # self.G = nx.Graph()
        self.nodes = []
        self.links = []
        self.max_weight = 1
    
    def parse_file(self,filename):
        obj=etree.parse(filename,etree.HTMLParser())
        body=obj.xpath('/html/body/*[name(.)!="script"]')
        self.get_children(body,str(self.name_idx))
        return {"nodes":self.nodes,"links":self.links}

    def parse(self,html):
        obj=etree.HTML(html)
        body=obj.xpath('/html/body/*[name(.)!="script"]')
        self.nodes.append({"id":str(self.name_idx),"size":2.5})
        self.get_children(body,str(self.name_idx))
        return {"nodes":self.nodes,"links":self.links}

    def get_children(self,node,parent_name):
        # children = []
        self.max_weight += 1
        for elm in node:
            self.name_idx += 1
            if type(elm.tag)!=str: continue
            node_name = str(self.name_idx) +": "+elm.tag
            if len(elm)==0:
                text = elm.xpath('string()')
                # print(text)
                # node_name += "["+ text+ "]"
            # child = {'name':node_name}
            # child['size'] = math.ceil(self.char_density(elm))
            node = {"id":node_name,"size":math.ceil(self.char_density(elm))}
            self.nodes.append(node)
            link = {"source":parent_name,"target":node_name}
            self.links.append(link)
            self.get_children(elm, node_name)
            # if len(this_children)!=0:
            #     child["children"] = this_children
            # children.append(child)
        # return children

    # 计算节点的字符密度
    def char_density(self,node):
        # 1. get word count
        text = node.xpath('string()')
        word_len = len(str(text))
        # 2. tag <a> word count
        a = node.xpath('.//a')
        a_text = ''
        for n in a:
            a_text += n.xpath('string()')
        a_len = len(a_text)
        # 3. get all children
        children = node.xpath('//*')
        children_count = len(children)
        # 4. get a count
        a_count = len(a)
        # 5. compute
        print(word_len,a_len,children_count,a_count)
        return (word_len-a_len)/(children_count-a_count)

# dt = DomTree()
# result = dt.parse_file('test.html')
# print(result)
# with open('tieba.json', 'w') as fw:
#     json.dump(result,fw)
# print(result)
# get_children(G,result,name_idx)
# nx.draw(G,with_labels=True)
# plt.show()