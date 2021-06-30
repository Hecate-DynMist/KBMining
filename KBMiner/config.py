from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pandas as pd
from flashtext import KeywordProcessor
keyword_processor = KeywordProcessor()
import numpy as np
import collections
from datetime import datetime
# 自定义匹配词条
def keydict(dfo,colo):
    for term in dfo[colo]:
        keyword_processor.add_keyword(term)
# 全匹配
def fullmatch(term):
    return keyword_processor.extract_keywords(term)

# 根据词权重不同和词频计算分数
def score(df,key,value,list):
    dic = dict(zip(df[key], df[value]))
    return sum([dic[k] for k in dic.keys() if k in list])

# 技术词源预处理
graph = Graph("bolt://localhost:7687", user="neo4j", password="lene1111")  # 在此处修改为本地neo4j的端口，用户名和密码
base = pd.read_excel('./Inputs/Base.xlsx').fillna(1)  # 技术词源，修改为本地的路径文件即可
keydict(base, 'Key')  # 功能型函数，不需要修改
techbase = base  # 不适用kb的扩展词匹配
# techbase = techexpand('n') # 使用kb的扩展词匹配