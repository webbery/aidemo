from lxml import etree
# import networkx as nx
# import matplotlib.pyplot as plt
import json

class DomTree():
    def __init__(self):
        self.name_idx = 1
        # self.G = nx.Graph()
        self.graph={}
        self.max_weight = 1
    
    def parse_file(self,filename):
        obj=etree.parse(filename,etree.HTMLParser())
        body=obj.xpath('/html/body/*[name(.)!="script"]')
        return {
            'name':'root',
            'children':self.get_children(body,self.name_idx)
        }

    def parse(self,html):
        # obj=etree.HTML(html)
        # body=obj.xpath('/html/body/*[name(.)!="script"]')
        # self.get_children(body,self.name_idx)
        # return self.parse_file('test.html')
        return self.parse_file('tieba.html')

    def get_children(self,node,parent_name):
        children = []
        self.max_weight += 1
        for elm in node:
            self.name_idx += 1
            if type(elm.tag)!=str: continue
            node_name = str(self.name_idx) +": "+elm.tag
            if len(elm)==0:
                text = elm.xpath('string()')
                # print(text)
                # node_name += "["+ text+ "]"
            child = {'name':node_name}
            this_children = self.get_children(elm, node_name)
            if len(this_children)!=0:
                child["children"] = this_children
            children.append(child)
        return children

    def char_density(self,node):
        pass

# dt = DomTree()
# result = dt.parse_file('tieba.html')
# with open('tieba.json', 'w') as fw:
#     json.dump(result,fw)
# print(result)
# get_children(G,result,name_idx)
# nx.draw(G,with_labels=True)
# plt.show()