﻿# from requests_html import HTMLSession
import json
import re
from collections import defaultdict

# session = HTMLSession()
# r = session.get("https://www.bjsubway.com/station/zjgls", verify=False)
# print('=======')
# structure of stations: {
#   xxx_station:{
#       neighbor:[{name:xxx,distance:xxx}],
#       subway:subway_name
#   }
# }

#爬虫数据
stations={"苹果园": {"subway": ["1号线"], "neighbor": [{"name": "古城", "distance": 2606}]}, "古城": {"subway": ["1号线"], "neighbor": [{"name": "苹果园", "distance": 2606}, {"name": "八角游乐园", "distance": 1921}]}, "八角游乐园": {"subway": ["1号线"], "neighbor": [{"name": "古城", "distance": 1921}, {"name": "八宝山", "distance": 1953}]}, "八宝山": {"subway": ["1号线"], "neighbor": [{"name": "八角游乐园", "distance": 1953}, {"name": "玉泉路", "distance": 1479}]}, "玉泉路": {"subway": ["1号线"], "neighbor": [{"name": "八宝山", "distance": 1479}, {"name": "五棵松", "distance": 1810}]}, "五棵松": {"subway": ["1号线"], "neighbor": [{"name": "玉泉路", "distance": 1810}, {"name": "万寿路", "distance": 1778}]}, "万寿路": {"subway": ["1号线"], "neighbor": [{"name": "五棵松", "distance": 1778}, {"name": "公主坟", "distance": 1313}]}, "公主坟": {"subway": ["1号线", "10号线"], "neighbor": [{"name": "万寿路", "distance": 1313}, {"name": "军事博物馆", "distance": 1172}, {"name": "莲花桥", "distance": 1016}, {"name": "西钓鱼台", "distance": 2386}]}, "军事博物馆": {"subway": ["1号线", "9号线"], "neighbor": [{"name": "公主坟", "distance": 1172}, {"name": "木樨地", "distance": 1166}, {"name": "白堆子", "distance": 1912}, {"name": "北京西站", "distance": 1398}]}, "木樨地": {"subway": ["1号线"], "neighbor": [{"name": "军事博物馆", "distance": 1166}, {"name": "南礼士路", "distance": 1291}]}, "南礼士路": {"subway": ["1号线"], "neighbor": [{"name": "木樨地", "distance": 1291}, {"name": "复兴门", "distance": 424}]}, "复兴门": {"subway": ["1号线", "2号线"], "neighbor": [{"name": "南礼士路", "distance": 424}, {"name": "西单", "distance": 1590}, {"name": "阜成门", "distance": 1832}, {"name": "长椿街", "distance": 1234}]}, "西单": {"subway": ["1号线", "4号线"], "neighbor": [{"name": "复兴门", "distance": 1590}, {"name": "天安门西", "distance": 1217}, {"name": "灵境胡同", "distance": 1011}, {"name": "宣武门", "distance": 815}]}, "天安门西": {"subway": ["1号线"], "neighbor": [{"name": "西单", "distance": 1217}, {"name": "天安门东", "distance": 925}]}, "天安门东": {"subway": ["1号线"], "neighbor": [{"name": "天安门西", "distance": 925}, {"name": "王府井", "distance": 852}]}, "王府井": {"subway": ["1号线"], "neighbor": [{"name": "天安门东", "distance": 852}, {"name": "东单", "distance": 774}]}, "东单": {"subway": ["1号线", "5号线"], "neighbor": [{"name": "王府井", "distance": 774}, {"name": "建国门", "distance": 1230}, {"name": "灯市口", "distance": 945}, {"name": "崇文门", "distance": 821}]}, "建国门": {"subway": ["1号线", "2号线"], "neighbor": [{"name": "东单", "distance": 1230}, {"name": "永安里", "distance": 1377}, {"name": "北京站", "distance": 945}, {"name": "朝阳门", "distance": 1763}]}, "永安里": {"subway": ["1号线"], "neighbor": [{"name": "建国门", "distance": 1377}, {"name": "国贸", "distance": 790}]}, "国贸": {"subway": ["1号线", "10号线"], "neighbor": [{"name": "永安里", "distance": 790}, {"name": "大望路", "distance": 1385}, {"name": "金台夕照", "distance": 835}, {"name": "双井", "distance": 1759}]}, "大望路": {"subway": ["1号线", "14号线（东段）"], "neighbor": [{"name": "国贸", "distance": 1385}, {"name": "四惠", "distance": 1673}, {"name": "九龙山", "distance": 1780}, {"name": "红庙", "distance": 708}]}, "四惠": {"subway": ["1号线", "八通线"], "neighbor": [{"name": "大望路", "distance": 1673}, {"name": "四惠东", "distance": 1714}, {"name": "四惠东", "distance": 1715}]}, "四惠东": {"subway": ["1号线", "八通线"], "neighbor": [{"name": "四惠", "distance": 1714}, {"name": "四惠", "distance": 1715}, {"name": "高碑店", "distance": 1375}]}, "西直门": {"subway": ["2号线", "4号线", "13号线"], "neighbor": [{"name": "车公庄", "distance": 909}, {"name": "积水潭", "distance": 1899}, {"name": "动物园", "distance": 1441}, {"name": "新街口", "distance": 1025}, {"name": "大钟寺", "distance": 2839}]}, "车公庄": {"subway": ["2号线", "6号线"], "neighbor": [{"name": "西直门", "distance": 909}, {"name": "阜成门", "distance": 960}, {"name": "车公庄西", "distance": 887}, {"name": "平安里", "distance": 1443}]}, "阜成门": {"subway": ["2号线"], "neighbor": [{"name": "车公庄", "distance": 960}, {"name": "复兴门", "distance": 1832}]}, "长椿街": {"subway": ["2号线"], "neighbor": [{"name": "复兴门", "distance": 1234}, {"name": "宣武门", "distance": 929}]}, "宣武门": {"subway": ["2号线", "4号线"], "neighbor": [{"name": "长椿街", "distance": 929}, {"name": "和平门", "distance": 851}, {"name": "西单", "distance": 815}, {"name": "菜市口", "distance": 1152}]}, "和平门": {"subway": ["2号线"], "neighbor": [{"name": "宣武门", "distance": 851}, {"name": "前门", "distance": 1171}]}, "前门": {"subway": ["2号线"], "neighbor": [{"name": "和平门", "distance": 1171}, {"name": "崇文门", "distance": 1634}]}, "崇文门": {"subway": ["2号线", "5号线"], "neighbor": [{"name": "前门", "distance": 1634}, {"name": "北京站", "distance": 1023}, {"name": "东单", "distance": 821}, {"name": "磁器口", "distance": 876}]}, "北京站": {"subway": ["2号线"], "neighbor": [{"name": "崇文门", "distance": 1023}, {"name": "建国门", "distance": 945}]}, "朝阳门": {"subway": ["2号线", "6号线"], "neighbor": [{"name": "建国门", "distance": 1763}, {"name": "东四十条", "distance": 1027}, {"name": "东四", "distance": 1399}, {"name": "东大桥", "distance": 1668}]}, "东四十条": {"subway": ["2号线"], "neighbor": [{"name": "朝阳门", "distance": 1027}, {"name": "东直门", "distance": 824}]}, "东直门": {"subway": ["2号线", "13号线", "机场线"], "neighbor": [{"name": "东四十条", "distance": 824}, {"name": "雍和宫", "distance": 2228}, {"name": "柳芳", "distance": 1769}, {"name": "三元桥", "distance": 2999}]}, "雍和宫": {"subway": ["2号线", "5号线"], "neighbor": [{"name": "东直门", "distance": 2228}, {"name": "安定门", "distance": 794}, {"name": "和平里北街", "distance": 1151}, {"name": "北新桥", "distance": 866}]}, "安定门": {"subway": ["2号线"], "neighbor": [{"name": "雍和宫", "distance": 794}, {"name": "鼓楼大街", "distance": 1237}]}, "鼓楼大街": {"subway": ["2号线", "8号线"], "neighbor": [{"name": "安定门", "distance": 1237}, {"name": "积水潭", "distance": 1766}, {"name": "安德里北街", "distance": 1083}, {"name": "什刹海", "distance": 1188}]}, "积水潭": {"subway": ["2号线"], "neighbor": [{"name": "鼓楼大街", "distance": 1766}, {"name": "西直门", "distance": 1899}]}, "安河桥北": {"subway": ["4号线"], "neighbor": [{"name": "北宫门", "distance": 1363}]}, "北宫门": {"subway": ["4号线"], "neighbor": [{"name": "安河桥北", "distance": 1363}, {"name": "西苑", "distance": 1251}]}, "西苑": {"subway": ["4号线"], "neighbor": [{"name": "北宫门", "distance": 1251}, {"name": "圆明园", "distance": 1672}]}, "圆明园": {"subway": ["4号线"], "neighbor": [{"name": "西苑", "distance": 1672}, {"name": "北京大学东门", "distance": 1295}]}, "北京大学东门": {"subway": ["4号线"], "neighbor": [{"name": "圆明园", "distance": 1295}, {"name": "中关村", "distance": 887}]}, "中关村": {"subway": ["4号线"], "neighbor": [{"name": "北京大学东门", "distance": 887}, {"name": "海淀黄庄", "distance": 900}]}, "海淀黄庄": {"subway": ["4号线", "10号线"], "neighbor": [{"name": "中关村", "distance": 900}, {"name": "人民大学", "distance": 1063}, {"name": "苏州街", "distance": 950}, {"name": "知春里", "distance": 975}]}, "人民大学": {"subway": ["4号线"], "neighbor": [{"name": "海淀黄庄", "distance": 1063}, {"name": "魏公村", "distance": 1051}]}, "魏公村": {"subway": ["4号线"], "neighbor": [{"name": "人民大学", "distance": 1051}, {"name": "国家图书馆", "distance": 1658}]}, "国家图书馆": {"subway": ["4号线", "9号线"], "neighbor": [{"name": "魏公村", "distance": 1658}, {"name": "动物园", "distance": 1517}, {"name": "白石桥南", "distance": 1096}]}, "动物园": {"subway": ["4号线"], "neighbor": [{"name": "国家图书馆", "distance": 1517}, {"name": "西直门", "distance": 1441}]}, "新街口": {"subway": ["4号线"], "neighbor": [{"name": "西直门", "distance": 1025}, {"name": "平安里", "distance": 1100}]}, "平安里": {"subway": ["4号线", "6号线"], "neighbor": [{"name": "新街口", "distance": 1100}, {"name": "西四", "distance": 1100}, {"name": "车公庄", "distance": 1443}, {"name": "北海北", "distance": 1321}]}, "西四": {"subway": ["4号线"], "neighbor": [{"name": "平安里", "distance": 1100}, {"name": "灵境胡同", "distance": 869}]}, "灵境胡同": {"subway": ["4号线"], "neighbor": [{"name": "西四", "distance": 869}, {"name": "西单", "distance": 1011}]}, "菜市口": {"subway": ["4号线", "7号线"], "neighbor": [{"name": "宣武门", "distance": 1152}, {"name": "陶然亭", "distance": 1200}, {"name": "广安门内", "distance": 1374}, {"name": "虎坊桥", "distance": 885}]}, "陶然亭": {"subway": ["4号线"], "neighbor": [{"name": "菜市口", "distance": 1200}, {"name": "北京南站", "distance": 1643}]}, "北京南站": {"subway": ["4号线", "14号线（东段）"], "neighbor": [{"name": "陶然亭", "distance": 1643}, {"name": "马家堡", "distance": 1480}, {"name": "陶然桥", "distance": 887}]}, "马家堡": {"subway": ["4号线"], "neighbor": [{"name": "北京南站", "distance": 1480}, {"name": "角门西", "distance": 827}]}, "角门西": {"subway": ["4号线", "10号线"], "neighbor": [{"name": "马家堡", "distance": 827}, {"name": "公益西桥", "distance": 989}, {"name": "角门东", "distance": 1254}, {"name": "草桥", "distance": 1688}]}, "公益西桥": {"subway": ["4号线", "大兴线"], "neighbor": [{"name": "角门西", "distance": 989}, {"name": "新宫", "distance": 2798}]}, "天通苑北": {"subway": ["5号线"], "neighbor": [{"name": "天通苑", "distance": 939}]}, "天通苑": {"subway": ["5号线"], "neighbor": [{"name": "天通苑北", "distance": 939}, {"name": "天通苑南", "distance": 965}]}, "天通苑南": {"subway": ["5号线"], "neighbor": [{"name": "天通苑", "distance": 965}, {"name": "立水桥", "distance": 1544}]}, "立水桥": {"subway": ["5号线", "13号线"], "neighbor": [{"name": "天通苑南", "distance": 1544}, {"name": "立水桥南", "distance": 1305}, {"name": "霍营", "distance": 4785}, {"name": "北苑", "distance": 2272}]}, "立水桥南": {"subway": ["5号线"], "neighbor": [{"name": "立水桥", "distance": 1305}, {"name": "北苑路北", "distance": 1286}]}, "北苑路北": {"subway": ["5号线"], "neighbor": [{"name": "立水桥南", "distance": 1286}, {"name": "大屯路东", "distance": 3000}]}, "大屯路东": {"subway": ["5号线", "15号线"], "neighbor": [{"name": "北苑路北", "distance": 3000}, {"name": "惠新西街北口", "distance": 1838}, {"name": "安立路", "distance": 938}, {"name": "关庄", "distance": 1087}]}, "惠新西街北口": {"subway": ["5号线"], "neighbor": [{"name": "大屯路东", "distance": 1838}, {"name": "惠新西街南口", "distance": 1122}]}, "惠新西街南口": {"subway": ["5号线", "10号线"], "neighbor": [{"name": "惠新西街北口", "distance": 1122}, {"name": "和平西桥", "distance": 1025}, {"name": "安贞门", "distance": 982}, {"name": "芍药居", "distance": 1712}]}, "和平西桥": {"subway": ["5号线"], "neighbor": [{"name": "惠新西街南口", "distance": 1025}, {"name": "和平里北街", "distance": 1059}]}, "和平里北街": {"subway": ["5号线"], "neighbor": [{"name": "和平西桥", "distance": 1059}, {"name": "雍和宫", "distance": 1151}]}, "北新桥": {"subway": ["5号线"], "neighbor": [{"name": "雍和宫", "distance": 866}, {"name": "张自忠路", "distance": 791}]}, "张自忠路": {"subway": ["5号线"], "neighbor": [{"name": "北新桥", "distance": 791}, {"name": "东四", "distance": 1016}]}, "东四": {"subway": ["5号线", "6号线"], "neighbor": [{"name": "张自忠路", "distance": 1016}, {"name": "灯市口", "distance": 848}, {"name": "南锣鼓巷", "distance": 1937}, {"name": "朝阳门", "distance": 1399}]}, "灯市口": {"subway": ["5号线"], "neighbor": [{"name": "东四", "distance": 848}, {"name": "东单", "distance": 945}]}, "磁器口": {"subway": ["5号线", "7号线"], "neighbor": [{"name": "崇文门", "distance": 876}, {"name": "天坛东门", "distance": 1183}, {"name": "桥湾", "distance": 1016}, {"name": "广渠门内", "distance": 1138}]}, "天坛东门": {"subway": ["5号线"], "neighbor": [{"name": "磁器口", "distance": 1183}, {"name": "蒲黄榆", "distance": 1900}]}, "蒲黄榆": {"subway": ["5号线", "14号线（东段）"], "neighbor": [{"name": "天坛东门", "distance": 1900}, {"name": "刘家窑", "distance": 905}, {"name": "景泰", "distance": 1025}, {"name": "方庄", "distance": 1486}]}, "刘家窑": {"subway": ["5号线"], "neighbor": [{"name": "蒲黄榆", "distance": 905}, {"name": "宋家庄", "distance": 1670}]}, "宋家庄": {"subway": ["5号线", "10号线", "亦庄线"], "neighbor": [{"name": "刘家窑", "distance": 1670}, {"name": "成寿寺", "distance": 1677}, {"name": "石榴庄", "distance": 1269}, {"name": "肖村", "distance": 2631}]}, "海淀五路居": {"subway": ["6号线"], "neighbor": [{"name": "慈寿寺", "distance": 1508}]}, "慈寿寺": {"subway": ["6号线", "10号线"], "neighbor": [{"name": "海淀五路居", "distance": 1508}, {"name": "花园桥", "distance": 1431}, {"name": "西钓鱼台", "distance": 1214}, {"name": "车道沟", "distance": 1590}]}, "花园桥": {"subway": ["6号线"], "neighbor": [{"name": "慈寿寺", "distance": 1431}, {"name": "白石桥南", "distance": 1166}]}, "白石桥南": {"subway": ["6号线", "9号线"], "neighbor": [{"name": "花园桥", "distance": 1166}, {"name": "车公庄西", "distance": 1664}, {"name": "国家图书馆", "distance": 1096}, {"name": "白堆子", "distance": 943}]}, "车公庄西": {"subway": ["6号线"], "neighbor": [{"name": "白石桥南", "distance": 1664}, {"name": "车公庄", "distance": 887}]}, "北海北": {"subway": ["6号线"], "neighbor": [{"name": "平安里", "distance": 1321}, {"name": "南锣鼓巷", "distance": 1349}]}, "南锣鼓巷": {"subway": ["6号线", "8号线"], "neighbor": [{"name": "北海北", "distance": 1349}, {"name": "东四", "distance": 1937}, {"name": "什刹海", "distance": 902}]}, "东大桥": {"subway": ["6号线"], "neighbor": [{"name": "朝阳门", "distance": 1668}, {"name": "呼家楼", "distance": 845}]}, "呼家楼": {"subway": ["6号线", "10号线"], "neighbor": [{"name": "东大桥", "distance": 845}, {"name": "金台路", "distance": 1450}, {"name": "团结湖", "distance": 1149}, {"name": "金台夕照", "distance": 734}]}, "金台路": {"subway": ["6号线", "14号线（东段）"], "neighbor": [{"name": "呼家楼", "distance": 1450}, {"name": "十里堡", "distance": 2036}, {"name": "红庙", "distance": 894}, {"name": "朝阳公园", "distance": 1085}]}, "十里堡": {"subway": ["6号线"], "neighbor": [{"name": "金台路", "distance": 2036}, {"name": "青年路", "distance": 1282}]}, "青年路": {"subway": ["6号线"], "neighbor": [{"name": "十里堡", "distance": 1282}, {"name": "褡裢坡", "distance": 3999}]}, "褡裢坡": {"subway": ["6号线"], "neighbor": [{"name": "青年路", "distance": 3999}, {"name": "黄渠", "distance": 1238}]}, "黄渠": {"subway": ["6号线"], "neighbor": [{"name": "褡裢坡", "distance": 1238}, {"name": "常营", "distance": 1854}]}, "常营": {"subway": ["6号线"], "neighbor": [{"name": "黄渠", "distance": 1854}, {"name": "草房", "distance": 1405}]}, "草房": {"subway": ["6号线"], "neighbor": [{"name": "常营", "distance": 1405}, {"name": "物资学院路", "distance": 2115}]}, "物资学院路": {"subway": ["6号线"], "neighbor": [{"name": "草房", "distance": 2115}, {"name": "通州北关", "distance": 2557}]}, "通州北关": {"subway": ["6号线"], "neighbor": [{"name": "物资学院路", "distance": 2557}, {"name": "通运门", "distance": 1468}]}, "通运门": {"subway": ["6号线"], "neighbor": [{"name": "通州北关", "distance": 1468}, {"name": "北运河西", "distance": 1543}]}, "北运河西": {"subway": ["6号线"], "neighbor": [{"name": "通运门", "distance": 1543}, {"name": "北运河东", "distance": 1599}]}, "北运河东": {"subway": ["6号线"], "neighbor": [{"name": "北运河西", "distance": 1599}, {"name": "郝家府", "distance": 929}]}, "郝家府": {"subway": ["6号线"], "neighbor": [{"name": "北运河东", "distance": 929}, {"name": "东夏园", "distance": 1346}]}, "东夏园": {"subway": ["6号线"], "neighbor": [{"name": "郝家府", "distance": 1346}, {"name": "潞城", "distance": 1194}]}, "潞城": {"subway": ["6号线"], "neighbor": [{"name": "东夏园", "distance": 1194}]}, "朱辛庄": {"subway": ["8号线", "昌平线"], "neighbor": [{"name": "育知路", "distance": 2318}, {"name": "巩华城", "distance": 3799}, {"name": "生命科学园", "distance": 2367}]}, "育知路": {"subway": ["8号线"], "neighbor": [{"name": "朱辛庄", "distance": 2318}, {"name": "平西府", "distance": 1985}]}, "平西府": {"subway": ["8号线"], "neighbor": [{"name": "育知路", "distance": 1985}, {"name": "回龙观东大街", "distance": 2056}]}, "回龙观东大街": {"subway": ["8号线"], "neighbor": [{"name": "平西府", "distance": 2056}, {"name": "霍营", "distance": 1114}]}, "霍营": {"subway": ["8号线", "13号线"], "neighbor": [{"name": "回龙观东大街", "distance": 1114}, {"name": "育新", "distance": 1894}, {"name": "回龙观", "distance": 2110}, {"name": "立水桥", "distance": 4785}]}, "育新": {"subway": ["8号线"], "neighbor": [{"name": "霍营", "distance": 1894}, {"name": "西小口", "distance": 1543}]}, "西小口": {"subway": ["8号线"], "neighbor": [{"name": "育新", "distance": 1543}, {"name": "永泰庄", "distance": 1041}]}, "永泰庄": {"subway": ["8号线"], "neighbor": [{"name": "西小口", "distance": 1041}, {"name": "林萃桥", "distance": 2553}]}, "林萃桥": {"subway": ["8号线"], "neighbor": [{"name": "永泰庄", "distance": 2553}, {"name": "森林公园南门", "distance": 2555}]}, "森林公园南门": {"subway": ["8号线"], "neighbor": [{"name": "林萃桥", "distance": 2555}, {"name": "奥林匹克公园", "distance": 1016}]}, "奥林匹克公园": {"subway": ["8号线", "15号线"], "neighbor": [{"name": "森林公园南门", "distance": 1016}, {"name": "奥体中心", "distance": 1667}, {"name": "北沙滩", "distance": 1999}, {"name": "安立路", "distance": 1368}]}, "奥体中心": {"subway": ["8号线"], "neighbor": [{"name": "奥林匹克公园", "distance": 1667}, {"name": "北土城", "distance": 900}]}, "北土城": {"subway": ["8号线", "10号线"], "neighbor": [{"name": "奥体中心", "distance": 900}, {"name": "安华桥", "distance": 1018}, {"name": "健德门", "distance": 1100}, {"name": "安贞门", "distance": 1020}]}, "安华桥": {"subway": ["8号线"], "neighbor": [{"name": "北土城", "distance": 1018}, {"name": "安德里北街", "distance": 1274}]}, "安德里北街": {"subway": ["8号线"], "neighbor": [{"name": "安华桥", "distance": 1274}, {"name": "鼓楼大街", "distance": 1083}]}, "什刹海": {"subway": ["8号线"], "neighbor": [{"name": "鼓楼大街", "distance": 1188}, {"name": "南锣鼓巷", "distance": 902}]}, "白堆子": {"subway": ["9号线"], "neighbor": [{"name": "白石桥南", "distance": 943}, {"name": "军事博物馆", "distance": 1912}]}, "北京西站": {"subway": ["9号线", "7号线"], "neighbor": [{"name": "军事博物馆", "distance": 1398}, {"name": "六里桥东", "distance": 1170}, {"name": "湾子", "distance": 935}]}, "六里桥东": {"subway": ["9号线"], "neighbor": [{"name": "北京西站", "distance": 1170}, {"name": "六里桥", "distance": 1309}]}, "六里桥": {"subway": ["9号线", "10号线"], "neighbor": [{"name": "六里桥东", "distance": 1309}, {"name": "七里庄", "distance": 1778}, {"name": "西局", "distance": 1584}, {"name": "莲花桥", "distance": 2392}]}, "七里庄": {"subway": ["9号线", "14号线(西段)"], "neighbor": [{"name": "六里桥", "distance": 1778}, {"name": "丰台东大街", "distance": 1325}, {"name": "大井", "distance": 1579}, {"name": "西局", "distance": 845}]}, "丰台东大街": {"subway": ["9号线"], "neighbor": [{"name": "七里庄", "distance": 1325}, {"name": "丰台南路", "distance": 1585}]}, "丰台南路": {"subway": ["9号线"], "neighbor": [{"name": "丰台东大街", "distance": 1585}, {"name": "科怡路", "distance": 980}]}, "科怡路": {"subway": ["9号线"], "neighbor": [{"name": "丰台南路", "distance": 980}, {"name": "丰台科技园", "distance": 788}]}, "丰台科技园": {"subway": ["9号线"], "neighbor": [{"name": "科怡路", "distance": 788}, {"name": "郭公庄", "distance": 1347}]}, "郭公庄": {"subway": ["9号线", "房山线"], "neighbor": [{"name": "丰台科技园", "distance": 1347}, {"name": "大葆台", "distance": 1405}]}, "巴沟": {"subway": ["10号线"], "neighbor": [{"name": "苏州街", "distance": 1110}, {"name": "火器营", "distance": 1495}]}, "苏州街": {"subway": ["10号线"], "neighbor": [{"name": "巴沟", "distance": 1110}, {"name": "海淀黄庄", "distance": 950}]}, "知春里": {"subway": ["10号线"], "neighbor": [{"name": "海淀黄庄", "distance": 975}, {"name": "知春路", "distance": 1058}]}, "知春路": {"subway": ["10号线", "13号线"], "neighbor": [{"name": "知春里", "distance": 1058}, {"name": "西土城", "distance": 1101}, {"name": "大钟寺", "distance": 1206}, {"name": "五道口", "distance": 1829}]}, "西土城": {"subway": ["10号线"], "neighbor": [{"name": "知春路", "distance": 1101}, {"name": "牡丹园", "distance": 1330}]}, "牡丹园": {"subway": ["10号线"], "neighbor": [{"name": "西土城", "distance": 1330}, {"name": "健德门", "distance": 973}]}, "健德门": {"subway": ["10号线"], "neighbor": [{"name": "牡丹园", "distance": 973}, {"name": "北土城", "distance": 1100}]}, "安贞门": {"subway": ["10号线"], "neighbor": [{"name": "北土城", "distance": 1020}, {"name": "惠新西街南口", "distance": 982}]}, "芍药居": {"subway": ["10号线", "13号线"], "neighbor": [{"name": "惠新西街南口", "distance": 1712}, {"name": "太阳宫", "distance": 1003}, {"name": "望京西", "distance": 2152}, {"name": "光熙门", "distance": 1110}]}, "太阳宫": {"subway": ["10号线"], "neighbor": [{"name": "芍药居", "distance": 1003}, {"name": "三元桥", "distance": 1759}]}, "三元桥": {"subway": ["10号线", "机场线"], "neighbor": [{"name": "太阳宫", "distance": 1759}, {"name": "亮马桥", "distance": 1506}, {"name": "东直门", "distance": 2999}, {"name": "T3航站楼", "distance": 18329}, {"name": "T2航站楼", "distance": 20619}]}, "亮马桥": {"subway": ["10号线"], "neighbor": [{"name": "三元桥", "distance": 1506}, {"name": "农业展览馆", "distance": 914}]}, "农业展览馆": {"subway": ["10号线"], "neighbor": [{"name": "亮马桥", "distance": 914}, {"name": "团结湖", "distance": 853}]}, "团结湖": {"subway": ["10号线"], "neighbor": [{"name": "农业展览馆", "distance": 853}, {"name": "呼家楼", "distance": 1149}]}, "金台夕照": {"subway": ["10号线"], "neighbor": [{"name": "呼家楼", "distance": 734}, {"name": "国贸", "distance": 835}]}, "双井": {"subway": ["10号线", "7号线"], "neighbor": [{"name": "国贸", "distance": 1759}, {"name": "劲松", "distance": 1006}, {"name": "广渠门外", "distance": 1241}, {"name": "九龙山", "distance": 1311}]}, "劲松": {"subway": ["10号线"], "neighbor": [{"name": "双井", "distance": 1006}, {"name": "潘家园", "distance": 1021}]}, "潘家园": {"subway": ["10号线"], "neighbor": [{"name": "劲松", "distance": 1021}, {"name": "十里河", "distance": 1097}]}, "十里河": {"subway": ["10号线", "14号线（东段）"], "neighbor": [{"name": "潘家园", "distance": 1097}, {"name": "分钟寺", "distance": 1804}, {"name": "方庄", "distance": 1618}, {"name": "南八里庄", "distance": 1147}]}, "分钟寺": {"subway": ["10号线"], "neighbor": [{"name": "十里河", "distance": 1804}, {"name": "成寿寺", "distance": 1058}]}, "成寿寺": {"subway": ["10号线"], "neighbor": [{"name": "分钟寺", "distance": 1058}, {"name": "宋家庄", "distance": 1677}]}, "石榴庄": {"subway": ["10号线"], "neighbor": [{"name": "宋家庄", "distance": 1269}, {"name": "大红门", "distance": 1244}]}, "大红门": {"subway": ["10号线"], "neighbor": [{"name": "石榴庄", "distance": 1244}, {"name": "角门东", "distance": 1130}]}, "角门东": {"subway": ["10号线"], "neighbor": [{"name": "大红门", "distance": 1130}, {"name": "角门西", "distance": 1254}]}, "草桥": {"subway": ["10号线"], "neighbor": [{"name": "角门西", "distance": 1688}, {"name": "纪家庙", "distance": 1547}]}, "纪家庙": {"subway": ["10号线"], "neighbor": [{"name": "草桥", "distance": 1547}, {"name": "首经贸", "distance": 1143}]}, "首经贸": {"subway": ["10号线"], "neighbor": [{"name": "纪家庙", "distance": 1143}, {"name": "丰台站", "distance": 1717}]}, "丰台站": {"subway": ["10号线"], "neighbor": [{"name": "首经贸", "distance": 1717}, {"name": "泥洼", "distance": 954}]}, "泥洼": {"subway": ["10号线"], "neighbor": [{"name": "丰台站", "distance": 954}, {"name": "西局", "distance": 749}]}, "西局": {"subway": ["10号线", "14号线(西段)"], "neighbor": [{"name": "泥洼", "distance": 749}, {"name": "六里桥", "distance": 1584}, {"name": "七里庄", "distance": 845}]}, "莲花桥": {"subway": ["10号线"], "neighbor": [{"name": "六里桥", "distance": 2392}, {"name": "公主坟", "distance": 1016}]}, "西钓鱼台": {"subway": ["10号线"], "neighbor": [{"name": "公主坟", "distance": 2386}, {"name": "慈寿寺", "distance": 1214}]}, "车道沟": {"subway": ["10号线"], "neighbor": [{"name": "慈寿寺", "distance": 1590}, {"name": "长春桥", "distance": 1205}]}, "长春桥": {"subway": ["10号线"], "neighbor": [{"name": "车道沟", "distance": 1205}, {"name": "火器营", "distance": 961}]}, "火器营": {"subway": ["10号线"], "neighbor": [{"name": "长春桥", "distance": 961}, {"name": "巴沟", "distance": 1495}]}, "大钟寺": {"subway": ["13号线"], "neighbor": [{"name": "西直门", "distance": 2839}, {"name": "知春路", "distance": 1206}]}, "五道口": {"subway": ["13号线"], "neighbor": [{"name": "知春路", "distance": 1829}, {"name": "上地", "distance": 4866}]}, "上地": {"subway": ["13号线"], "neighbor": [{"name": "五道口", "distance": 4866}, {"name": "西二旗", "distance": 2538}]}, "西二旗": {"subway": ["13号线", "昌平线"], "neighbor": [{"name": "上地", "distance": 2538}, {"name": "龙泽", "distance": 3623}, {"name": "生命科学园", "distance": 5440}]}, "龙泽": {"subway": ["13号线"], "neighbor": [{"name": "西二旗", "distance": 3623}, {"name": "回龙观", "distance": 1423}]}, "回龙观": {"subway": ["13号线"], "neighbor": [{"name": "龙泽", "distance": 1423}, {"name": "霍营", "distance": 2110}]}, "北苑": {"subway": ["13号线"], "neighbor": [{"name": "立水桥", "distance": 2272}, {"name": "望京西", "distance": 6720}]}, "望京西": {"subway": ["13号线", "15号线"], "neighbor": [{"name": "北苑", "distance": 6720}, {"name": "芍药居", "distance": 2152}, {"name": "关庄", "distance": 2071}, {"name": "望京", "distance": 1758}]}, "光熙门": {"subway": ["13号线"], "neighbor": [{"name": "芍药居", "distance": 1110}, {"name": "柳芳", "distance": 1135}]}, "柳芳": {"subway": ["13号线"], "neighbor": [{"name": "光熙门", "distance": 1135}, {"name": "东直门", "distance": 1769}]}, "张郭庄": {"subway": ["14号线(西段)"], "neighbor": [{"name": "园博园", "distance": 1345}]}, "园博园": {"subway": ["14号线(西段)"], "neighbor": [{"name": "张郭庄", "distance": 1345}, {"name": "大瓦窑", "distance": 4073}]}, "大瓦窑": {"subway": ["14号线(西段)"], "neighbor": [{"name": "园博园", "distance": 4073}, {"name": "郭庄子", "distance": 1236}]}, "郭庄子": {"subway": ["14号线(西段)"], "neighbor": [{"name": "大瓦窑", "distance": 1236}, {"name": "大井", "distance": 2044}]}, "大井": {"subway": ["14号线(西段)"], "neighbor": [{"name": "郭庄子", "distance": 2044}, {"name": "七里庄", "distance": 1579}]}, "陶然桥": {"subway": ["14号线（东段）"], "neighbor": [{"name": "北京南站", "distance": 887}, {"name": "永定门外", "distance": 1063}]}, "永定门外": {"subway": ["14号线（东段）"], "neighbor": [{"name": "陶然桥", "distance": 1063}, {"name": "景泰", "distance": 1119}]}, "景泰": {"subway": ["14号线（东段）"], "neighbor": [{"name": "永定门外", "distance": 1119}, {"name": "蒲黄榆", "distance": 1025}]}, "方庄": {"subway": ["14号线（东段）"], "neighbor": [{"name": "蒲黄榆", "distance": 1486}, {"name": "十里河", "distance": 1618}]}, "南八里庄": {"subway": ["14号线（东段）"], "neighbor": [{"name": "十里河", "distance": 1147}, {"name": "北工大西门", "distance": 1276}]}, "北工大西门": {"subway": ["14号线（东段）"], "neighbor": [{"name": "南八里庄", "distance": 1276}, {"name": "平乐园", "distance": 1128}]}, "平乐园": {"subway": ["14号线（东段）"], "neighbor": [{"name": "北工大西门", "distance": 1128}, {"name": "九龙山", "distance": 897}]}, "九龙山": {"subway": ["14号线（东段）", "7号线"], "neighbor": [{"name": "平乐园", "distance": 897}, {"name": "大望路", "distance": 1780}, {"name": "双井", "distance": 1311}, {"name": "大郊亭", "distance": 781}]}, "红庙": {"subway": ["14号线（东段）"], "neighbor": [{"name": "大望路", "distance": 708}, {"name": "金台路", "distance": 894}]}, "朝阳公园": {"subway": ["14号线（东段）"], "neighbor": [{"name": "金台路", "distance": 1085}, {"name": "枣营", "distance": 1221}]}, "枣营": {"subway": ["14号线（东段）"], "neighbor": [{"name": "朝阳公园", "distance": 1221}, {"name": "东风北桥", "distance": 2173}]}, "东风北桥": {"subway": ["14号线（东段）"], "neighbor": [{"name": "枣营", "distance": 2173}, {"name": "将台", "distance": 1600}]}, "将台": {"subway": ["14号线（东段）"], "neighbor": [{"name": "东风北桥", "distance": 1600}, {"name": "高家园", "distance": 1171}]}, "高家园": {"subway": ["14号线（东段）"], "neighbor": [{"name": "将台", "distance": 1171}, {"name": "望京南", "distance": 676}]}, "望京南": {"subway": ["14号线（东段）"], "neighbor": [{"name": "高家园", "distance": 676}, {"name": "阜通", "distance": 1168}]}, "阜通": {"subway": ["14号线（东段）"], "neighbor": [{"name": "望京南", "distance": 1168}, {"name": "望京", "distance": 903}]}, "望京": {"subway": ["14号线（东段）", "15号线"], "neighbor": [{"name": "阜通", "distance": 903}, {"name": "东湖渠", "distance": 1283}, {"name": "望京西", "distance": 1758}, {"name": "望京东", "distance": 1652}]}, "东湖渠": {"subway": ["14号线（东段）"], "neighbor": [{"name": "望京", "distance": 1283}, {"name": "来广营", "distance": 1100}]}, "来广营": {"subway": ["14号线（东段）"], "neighbor": [{"name": "东湖渠", "distance": 1100}, {"name": "善各庄", "distance": 1364}]}, "善各庄": {"subway": ["14号线（东段）"], "neighbor": [{"name": "来广营", "distance": 1364}]}, "清华东路西口": {"subway": ["15号线"], "neighbor": [{"name": "六道口", "distance": 1144}]}, "六道口": {"subway": ["15号线"], "neighbor": [{"name": "清华东路西口", "distance": 1144}, {"name": "北沙滩", "distance": 1337}]}, "北沙滩": {"subway": ["15号线"], "neighbor": [{"name": "六道口", "distance": 1337}, {"name": "奥林匹克公园", "distance": 1999}]}, "安立路": {"subway": ["15号线"], "neighbor": [{"name": "奥林匹克公园", "distance": 1368}, {"name": "大屯路东", "distance": 938}]}, "关庄": {"subway": ["15号线"], "neighbor": [{"name": "大屯路东", "distance": 1087}, {"name": "望京西", "distance": 2071}]}, "望京东": {"subway": ["15号线"], "neighbor": [{"name": "望京", "distance": 1652}, {"name": "崔各庄", "distance": 2295}]}, "崔各庄": {"subway": ["15号线"], "neighbor": [{"name": "望京东", "distance": 2295}, {"name": "马泉营", "distance": 2008}]}, "马泉营": {"subway": ["15号线"], "neighbor": [{"name": "崔各庄", "distance": 2008}, {"name": "孙河", "distance": 3309}]}, "孙河": {"subway": ["15号线"], "neighbor": [{"name": "马泉营", "distance": 3309}, {"name": "国展", "distance": 3386}]}, "国展": {"subway": ["15号线"], "neighbor": [{"name": "孙河", "distance": 3386}, {"name": "花梨坎", "distance": 1615}]}, "花梨坎": {"subway": ["15号线"], "neighbor": [{"name": "国展", "distance": 1615}, {"name": "后沙峪", "distance": 3354}]}, "后沙峪": {"subway": ["15号线"], "neighbor": [{"name": "花梨坎", "distance": 3354}, {"name": "南法信", "distance": 4576}]}, "南法信": {"subway": ["15号线"], "neighbor": [{"name": "后沙峪", "distance": 4576}, {"name": "石门", "distance": 2712}]}, "石门": {"subway": ["15号线"], "neighbor": [{"name": "南法信", "distance": 2712}, {"name": "顺义", "distance": 1331}]}, "顺义": {"subway": ["15号线"], "neighbor": [{"name": "石门", "distance": 1331}, {"name": "俸伯", "distance": 2441}]}, "俸伯": {"subway": ["15号线"], "neighbor": [{"name": "顺义", "distance": 2441}]}, "高碑店": {"subway": ["八通线"], "neighbor": [{"name": "四惠东", "distance": 1375}, {"name": "传媒大学", "distance": 2002}]}, "传媒大学": {"subway": ["八通线"], "neighbor": [{"name": "高碑店", "distance": 2002}, {"name": "双桥", "distance": 1894}]}, "双桥": {"subway": ["八通线"], "neighbor": [{"name": "传媒大学", "distance": 1894}, {"name": "管庄", "distance": 1912}]}, "管庄": {"subway": ["八通线"], "neighbor": [{"name": "双桥", "distance": 1912}, {"name": "八里桥", "distance": 1763}]}, "八里桥": {"subway": ["八通线"], "neighbor": [{"name": "管庄", "distance": 1763}, {"name": "通州北苑", "distance": 1700}]}, "通州北苑": {"subway": ["八通线"], "neighbor": [{"name": "八里桥", "distance": 1700}, {"name": "果园", "distance": 1465}]}, "果园": {"subway": ["八通线"], "neighbor": [{"name": "通州北苑", "distance": 1465}, {"name": "九棵树", "distance": 990}]}, "九棵树": {"subway": ["八通线"], "neighbor": [{"name": "果园", "distance": 990}, {"name": "梨园", "distance": 1225}]}, "梨园": {"subway": ["八通线"], "neighbor": [{"name": "九棵树", "distance": 1225}, {"name": "临河里", "distance": 1257}]}, "临河里": {"subway": ["八通线"], "neighbor": [{"name": "梨园", "distance": 1257}, {"name": "土桥", "distance": 776}]}, "土桥": {"subway": ["八通线"], "neighbor": [{"name": "临河里", "distance": 776}]}, "昌平西山口": {"subway": ["昌平线"], "neighbor": [{"name": "十三陵景区", "distance": 1213}]}, "十三陵景区": {"subway": ["昌平线"], "neighbor": [{"name": "昌平西山口", "distance": 1213}, {"name": "昌平", "distance": 3508}]}, "昌平": {"subway": ["昌平线"], "neighbor": [{"name": "十三陵景区", "distance": 3508}, {"name": "昌平东关", "distance": 2433}]}, "昌平东关": {"subway": ["昌平线"], "neighbor": [{"name": "昌平", "distance": 2433}, {"name": "北邵洼", "distance": 1683}]}, "北邵洼": {"subway": ["昌平线"], "neighbor": [{"name": "昌平东关", "distance": 1683}, {"name": "南邵", "distance": 1958}]}, "南邵": {"subway": ["昌平线"], "neighbor": [{"name": "北邵洼", "distance": 1958}, {"name": "沙河高教园", "distance": 5357}]}, "沙河高教园": {"subway": ["昌平线"], "neighbor": [{"name": "南邵", "distance": 5357}, {"name": "沙河", "distance": 1964}]}, "沙河": {"subway": ["昌平线"], "neighbor": [{"name": "沙河高教园", "distance": 1964}, {"name": "巩华城", "distance": 2025}]}, "巩华城": {"subway": ["昌平线"], "neighbor": [{"name": "沙河", "distance": 2025}, {"name": "朱辛庄", "distance": 3799}]}, "生命科学园": {"subway": ["昌平线"], "neighbor": [{"name": "朱辛庄", "distance": 2367}, {"name": "西二旗", "distance": 5440}]}, "肖村": {"subway": ["亦庄线"], "neighbor": [{"name": "宋家庄", "distance": 2631}, {"name": "小红门", "distance": 1275}]}, "小红门": {"subway": ["亦庄线"], "neighbor": [{"name": "肖村", "distance": 1275}, {"name": "旧宫", "distance": 2366}]}, "旧宫": {"subway": ["亦庄线"], "neighbor": [{"name": "小红门", "distance": 2366}, {"name": "亦庄桥", "distance": 1982}]}, "亦庄桥": {"subway": ["亦庄线"], "neighbor": [{"name": "旧宫", "distance": 1982}, {"name": "亦庄文化园", "distance": 993}]}, "亦庄文化园": {"subway": ["亦庄线"], "neighbor": [{"name": "亦庄桥", "distance": 993}, {"name": "万源街", "distance": 1728}]}, "万源街": {"subway": ["亦庄线"], "neighbor": [{"name": "亦庄文化园", "distance": 1728}, {"name": "荣京东街", "distance": 1090}]}, "荣京东街": {"subway": ["亦庄线"], "neighbor": [{"name": "万源街", "distance": 1090}, {"name": "荣昌东街", "distance": 1355}]}, "荣昌东街": {"subway": ["亦庄线"], "neighbor": [{"name": "荣京东街", "distance": 1355}, {"name": "同济南路", "distance": 2337}]}, "同济南路": {"subway": ["亦庄线"], "neighbor": [{"name": "荣昌东街", "distance": 2337}, {"name": "经海路", "distance": 2301}]}, "经海路": {"subway": ["亦庄线"], "neighbor": [{"name": "同济南路", "distance": 2301}, {"name": "次渠南", "distance": 2055}]}, "次渠南": {"subway": ["亦庄线"], "neighbor": [{"name": "经海路", "distance": 2055}, {"name": "次渠", "distance": 1281}]}, "次渠": {"subway": ["亦庄线"], "neighbor": [{"name": "次渠南", "distance": 1281}]}, "新宫": {"subway": ["大兴线"], "neighbor": [{"name": "公益西桥", "distance": 2798}, {"name": "西红门", "distance": 5102}]}, "西红门": {"subway": ["大兴线"], "neighbor": [{"name": "新宫", "distance": 5102}, {"name": "高米店北", "distance": 1810}]}, "高米店北": {"subway": ["大兴线"], "neighbor": [{"name": "西红门", "distance": 1810}, {"name": "高米店南", "distance": 1128}]}, "高米店南": {"subway": ["大兴线"], "neighbor": [{"name": "高米店北", "distance": 1128}, {"name": "枣园", "distance": 1096}]}, "枣园": {"subway": ["大兴线"], "neighbor": [{"name": "高米店南", "distance": 1096}, {"name": "清源路", "distance": 1200}]}, "清源路": {"subway": ["大兴线"], "neighbor": [{"name": "枣园", "distance": 1200}, {"name": "黄村西大街", "distance": 1214}]}, "黄村西大街": {"subway": ["大兴线"], "neighbor": [{"name": "清源路", "distance": 1214}, {"name": "黄村火车站", "distance": 987}]}, "黄村火车站": {"subway": ["大兴线"], "neighbor": [{"name": "黄村西大街", "distance": 987}, {"name": "义和庄", "distance": 2035}]}, "义和庄": {"subway": ["大兴线"], "neighbor": [{"name": "黄村火车站", "distance": 2035}, {"name": "生物医药基地", "distance": 2918}]}, "生物医药基地": {"subway": ["大兴线"], "neighbor": [{"name": "义和庄", "distance": 2918}, {"name": "天宫院", "distance": 1811}]}, "天宫院": {"subway": ["大兴线"], "neighbor": [{"name": "生物医药基地", "distance": 1811}]}, "大葆台": {"subway": ["房山线"], "neighbor": [{"name": "郭公庄", "distance": 1405}, {"name": "稻田", "distance": 6466}]}, "稻田": {"subway": ["房山线"], "neighbor": [{"name": "大葆台", "distance": 6466}, {"name": "长阳", "distance": 4041}]}, "长阳": {"subway": ["房山线"], "neighbor": [{"name": "稻田", "distance": 4041}, {"name": "篱笆房", "distance": 2150}]}, "篱笆房": {"subway": ["房山线"], "neighbor": [{"name": "长阳", "distance": 2150}, {"name": "广阳城", "distance": 1474}]}, "广阳城": {"subway": ["房山线"], "neighbor": [{"name": "篱笆房", "distance": 1474}, {"name": "良乡大学城北", "distance": 2003}]}, "良乡大学城北": {"subway": ["房山线"], "neighbor": [{"name": "广阳城", "distance": 2003}, {"name": "良乡大学城", "distance": 1188}]}, "良乡大学城": {"subway": ["房山线"], "neighbor": [{"name": "良乡大学城北", "distance": 1188}, {"name": "良乡大学城西", "distance": 1738}]}, "良乡大学城西": {"subway": ["房山线"], "neighbor": [{"name": "良乡大学城", "distance": 1738}, {"name": "良乡南关", "distance": 1332}]}, "良乡南关": {"subway": ["房山线"], "neighbor": [{"name": "良乡大学城西", "distance": 1332}, {"name": "苏庄", "distance": 1330}]}, "苏庄": {"subway": ["房山线"], "neighbor": [{"name": "良乡南关", "distance": 1330}]}, "T3航站楼": {"subway": ["机场线"], "neighbor": [{"name": "三元桥", "distance": 18329}, {"name": "T2航站楼", "distance": 7239}]}, "T2航站楼": {"subway": ["机场线"], "neighbor": [{"name": "T3航站楼", "distance": 7239}, {"name": "三元桥", "distance": 20619}]}, "湾子": {"subway": ["7号线"], "neighbor": [{"name": "北京西站", "distance": 935}, {"name": "达官营", "distance": 734}]}, "达官营": {"subway": ["7号线"], "neighbor": [{"name": "湾子", "distance": 734}, {"name": "广安门内", "distance": 1874}]}, "广安门内": {"subway": ["7号线"], "neighbor": [{"name": "达官营", "distance": 1874}, {"name": "菜市口", "distance": 1374}]}, "虎坊桥": {"subway": ["7号线"], "neighbor": [{"name": "菜市口", "distance": 885}, {"name": "珠市口", "distance": 1205}]}, "珠市口": {"subway": ["7号线"], "neighbor": [{"name": "虎坊桥", "distance": 1205}, {"name": "桥湾", "distance": 869}]}, "桥湾": {"subway": ["7号线"], "neighbor": [{"name": "珠市口", "distance": 869}, {"name": "磁器口", "distance": 1016}]}, "广渠门内": {"subway": ["7号线"], "neighbor": [{"name": "磁器口", "distance": 1138}, {"name": "广渠门外", "distance": 1332}]}, "广渠门外": {"subway": ["7号线"], "neighbor": [{"name": "广渠门内", "distance": 1332}, {"name": "双井", "distance": 1241}]}, "大郊亭": {"subway": ["7号线"], "neighbor": [{"name": "九龙山", "distance": 781}, {"name": "百子湾", "distance": 865}]}, "百子湾": {"subway": ["7号线"], "neighbor": [{"name": "大郊亭", "distance": 865}, {"name": "化工", "distance": 903}]}, "化工": {"subway": ["7号线"], "neighbor": [{"name": "百子湾", "distance": 903}, {"name": "南楼梓庄", "distance": 1464}]}, "南楼梓庄": {"subway": ["7号线"], "neighbor": [{"name": "化工", "distance": 1464}, {"name": "欢乐谷景区", "distance": 906}]}, "欢乐谷景区": {"subway": ["7号线"], "neighbor": [{"name": "南楼梓庄", "distance": 906}, {"name": "垡头", "distance": 1679}]}, "垡头": {"subway": ["7号线"], "neighbor": [{"name": "欢乐谷景区", "distance": 1679}, {"name": "双合", "distance": 1304}]}, "双合": {"subway": ["7号线"], "neighbor": [{"name": "垡头", "distance": 1304}, {"name": "焦化厂", "distance": 1021}]}, "焦化厂": {"subway": ["7号线"], "neighbor": [{"name": "双合", "distance": 1021}]}}

class EditDistance():
    """
    计算字符串 str1 和 str2 的编辑距离
    :param str1
    :param str2
    :return:
    """
    def __init__(self):
        self.edit={}

    def edit_dist_impl(self,str1,str2):
        k = str1+','+str2
        if self.edit.__contains__(k): return self.edit[k]
        
        l1 = len(str1)
        l2 = len(str2)
        if l1==0:
            self.edit[k] = l2
            return l2
        if l2==0:
            self.edit[k] = l1
            return l1
        flag = 0 if str1[l1-1]==str2[l2-1] else 1
        self.edit[k] = min(self.edit_dist_impl(str1[0:l1-1],str2)+1,
            self.edit_dist_impl(str1,str2[0:l2-1])+1,
            self.edit_dist_impl(str1[0:l1-1],str2[0:l2-1])+flag)
        # print(str1,str2,self.edit[k],flag)
        return self.edit[k]

    def edit_distance(self,str1,str2):
        return self.edit_dist_impl(str1,str2)
    
similar_name = defaultdict(list)
ed = EditDistance()
# 计算所有站点之间的编辑距离,把距离为1的站点保存起来,作为相似提示
for station1 in stations.keys():
    for station2 in stations.keys():
        if ed.edit_distance(station1,station2)==1:
            similar_name[station1].append(station2)
# print(similar_name)
# print(ed.edit_distance('北宫','北京'))

def find_similar(name):
    '''
    根据给定字符查找相似站点
    '''
    result = []
    for station in stations.keys():
        if ed.edit_distance(name,station)==1:
            result.append(station)
    return result

def add_station_detail(subway,station1,station2,distance):
    if station1 in stations:
        subways = stations[station1]['subway']
        if subway not in subways:
            subways.append(subway)
        stations[station1]['neighbor'].append({
            'name':station2,
            'distance':distance
        })
    else:
        stations[station1]={
            'subway':[subway],
            'neighbor':[{
                'name':station2,
                'distance':distance
            }]
        }

def add_station(subway,station1,station2,distance):
    add_station_detail(subway,station1,station2,distance)
    add_station_detail(subway,station2,station1,distance)

# for i in range(18):
#     regex_table = "#sub"+str(i)+" table"
#     # regex_table = "#sub"+str(9)+" table"
#     tables = r.html.find(regex_table)
#     for i_table in range(len(tables)):
#         data = tables[i_table].find("tr")
#         subway_name = ''
#         for idx in range(len(data)):
#             # print(data[idx].html)
#             if idx==1: continue     # do not process describe grid
            
#             # here we can use regex or css selector to get data
#             if idx==0:
#                 searchObj = re.search(r'.*<td .*>(.*)相邻站间距信息统计表</td>',data[idx].html,re.M|re.S)
#                 if searchObj:
#                     subway_name = searchObj.group(1)
#                     # print("searchObj.group(1) : ", searchObj.group(1))
#             else:
#                 searchObj = re.search(r'<th>(.*)——(.*)</th>\n<td(.*?)>(\w+)</td>',data[idx].html,re.M|re.S)
#                 if searchObj:
#                     station1 = searchObj.group(1)
#                     station2 = searchObj.group(2)
#                     distance = int(searchObj.group(4))
#                     add_station(subway_name,station1,station2,distance)
# with open("./hmm.json",'w',encoding='utf-8') as json_file:
#     json.dump(stations,json_file,ensure_ascii=False)

def BFS(start,dest):
    station1 = stations[start]

    path = []
    seen = []
    neighbors = station1['neighbor'][:]
    while len(neighbors)>0:
        front = neighbors.pop(0)
        if front['name'] in seen: continue
        
        seen.append(front['name'])
        print(front['name'])
        # print(front['name'],neighbors)
        if front['name']==dest:
            break
        neighbors = neighbors + stations[front['name']]['neighbor']
        
# BFS('西单','呼家楼')

def search_detail(start,dest,search_map,cost):
    result = None
    pathes = [{'path':[start],'distance':0,'subways':[]}]

    # visited = []
    while pathes:
        path = pathes.pop(0)
        station_name = path['path'][-1]

        neighbors = search_map[station_name]['neighbor']
        for neighbor in neighbors:
            if neighbor['name'] in path['path']: continue   # exclude loop path
            new_path = path['path'] + [neighbor['name']]
            subway = list(set(search_map[station_name]['subway'])&set(search_map[neighbor['name']]['subway']))
            new_subway =path['subways'] + (subway if subway[0] not in path['subways'] else [])
            path_info = {
                'path':new_path,
                'distance': path['distance']+neighbor['distance'],
                'subways': new_subway
            }
            # exclude path which is badder than results
            if result and cost(path_info)>cost(result): continue
            pathes.append(path_info)

            if neighbor['name']==dest:
                # print(path_info)
                result = path_info
                break
    return result

class TransferNum:
    def __init__(self,transfer,station):
        self.transfer_count=transfer
        self.station_count=station

    def __gt__(self, value):
        if self.transfer_count>value.transfer_count: return True
        #if self.station_count>value.station_count: return True
        return False

def station_count(obj):
    return len(obj['path'])

def transfer_count(obj):
    return TransferNum(len(obj['subways']),len(obj['path']))

def get_distance(obj):
    return obj['distance']

def is_exist(station):
    if not stations.__contains__(station):
        print(station+' not exist')
        return False
    return True

def get_tips(name):
    similar = find_similar(name)
    tips = ''
    if len(similar)!=0:
        tips = ',是否要查找'
        for station in similar: tips+=station+','
    return tips[0:len(tips)-1]

def search(src,dst,t=0):
    if not is_exist(src):
        return {'result':src+'站不存在'+get_tips(src)}
    if not is_exist(dst):
        return {'result':dst+'站不存在'+get_tips(dst)}
    if t==1:
        return search_detail(src,dst,stations,transfer_count)
    if t==2:
        return search_detail(src,dst,stations,get_distance)
    return search_detail(src,dst,stations,station_count)

# print(search('地坛','平西路'))

def a_star(start,dest,search_map,cost):
    result = None
    pathes = [{'path':[start],'distance':0,'subways':[]}]

    # visited = []
    while pathes:
        path = pathes.pop(0)
        station_name = path['path'][-1]

        neighbors = search_map[station_name]['neighbor']
        for neighbor in neighbors:
            if neighbor['name'] in path['path']: continue   # exclude loop path
            new_path = path['path'] + [neighbor['name']]
            subway = list(set(search_map[station_name]['subway'])&set(search_map[neighbor['name']]['subway']))
            new_subway =path['subways'] + (subway if subway[0] not in path['subways'] else [])
            path_info = {
                'path':new_path,
                'distance': path['distance']+neighbor['distance'],
                'subways': new_subway
            }
            # exclude path which is badder than results
            
            # if result and cost(path_info)>cost(result): continue
            # pathes.append(path_info)

            if neighbor['name']==dest:
                result = path_info
                break
    return result

# print(search('顺义','西土城'))
