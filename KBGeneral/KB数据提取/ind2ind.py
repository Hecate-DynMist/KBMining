from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pandas as pd
graph = Graph("bolt://localhost:7687", user="neo4j",password="lene1111")

def intoin(index):
    df1 = pd.DataFrame(graph.run('MATCH (a:Institution)-[]-(b:'+index+') RETURN a.name,b.name'),columns=['机构',index])
    df2 = pd.DataFrame(graph.run('MATCH (a:'+index+')-[]-(b:Institution) RETURN a.name,b.name'),columns=[index,'关联机构'])
    df2 = df2.groupby([index])['关联机构'].apply(set).reset_index()
    df = pd.merge(df1,df2,on=index,how='left')
    df = df.groupby(['机构'])['关联机构'].apply(lambda x: set.union(*x)).reset_index()
    df['关联机构数目'] = df['关联机构'].apply(lambda x:len(x))
    return df

def final():
    xls = pd.ExcelWriter('./Outputs/机构二级关联.xlsx')
    intoin('TechField').to_excel(xls,sheet_name='技术领域关联',index=False)
    intoin('AiField').to_excel(xls,sheet_name='智能领域关联',index=False)
    intoin('Industry').to_excel(xls, sheet_name='行业关联', index=False)
    xls.save()
    xls.close()

final()