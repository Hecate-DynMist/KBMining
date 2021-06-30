from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pandas as pd
graph = Graph("bolt://localhost:7687", user="neo4j",password="lene1111")
pd.set_option("display.max_columns", 100)
from datetime import datetime
def timeadjust(x):
    try:
        return datetime.fromtimestamp(x).strftime('%Y-%m-%d')
    except:
        return None

# 实体特定属性
def pureproperty(enti,column):
    column1 = enti.split()+column.split(',')
    if enti == 'Institution':
        pty = pd.DataFrame(graph.run(
            'MATCH (a:Institution) RETURN a.uuid,a.name,a.summary,a.roles,a.core_tech,a.financing_round,a.founded_at,a.companySize,a.region,a.round_scope'), \
                           columns=['uuid', 'Institution', 'summary', 'roles', 'core_tech', 'financing_round',
                                    'founded_at','companySize','region','round_scope'])[column1]
    elif enti == 'Solution':
        pty = pd.DataFrame(graph.run('MATCH (a:Solution) RETURN a.uuid,a.name,a.summary,a.core_tech'),columns=['uuid','Solution','summary','core_tech'])[enti,column]
    elif enti == 'BusinessCase':
        pty = pd.DataFrame(graph.run('MATCH (a:BusinessCase) RETURN a.uuid,a.name,a.core_tech'),
                           columns=['uuid', 'BusinessCase', 'core_tech'])[column1]
    else:
        pty = pd.DataFrame()
    pty.to_excel('./Outputs/'+enti+'-'+column+'.xlsx',index=False)
    return pty

# 一级关系提取
def relation1(enti1,enti2):
    df = pd.DataFrame(graph.run('MATCH (a:'+enti1+')-[]-(c:' + enti2 + ') RETURN a.name,c.name'),columns=[enti1, enti2])
    df = df.drop_duplicates()
    dfa = df.groupby(enti1)[enti2].apply(list).reset_index()
    dfa.to_excel('./Outputs/'+enti1+'-'+ enti2 +'.xlsx', index=False)
    return df

# 提取实体，若有别名提取别名
def extract(entity,alias):
    if alias == 'y':
        enti1 = pd.DataFrame(graph.run('MATCH (b)-[r:alias_of]->(n:'+entity+') RETURN n.name,b.name,labels(n)'),columns=[entity,'alias','label'])
        enti1 = enti1.groupby([entity]).agg(alias=('alias',lambda x: ','.join(set(x))),label=('label','sum')).reset_index()
        enti1['label'] = enti1['label'].apply(lambda x:list(set(x)))
        enti2 = pd.DataFrame(graph.run('MATCH (n:'+entity+') WHERE NOT (n)<-[:alias_of]-() AND NOT (n)-[:alias_of]->() Return n.name,labels(n)'),
                     columns=[entity,'label'])
        enti2 = enti2.groupby([entity]).agg(label=('label','sum')).reset_index()
        enti1['label'] = enti1['label'].apply(lambda x: list(set(x)))
        # enti2r = pd.Series([i for i in map(str.lower,enti2[entity].to_list()) if i.lower() not in map(str.lower,enti1[entity].to_list())])
        enti2r = pd.DataFrame([i for i in enti2[entity].to_list() if i not in enti1[entity].to_list()],columns=[entity])
        enti2rr = pd.merge(enti2r,enti2,how='left',on=entity)
        enti1 = pd.concat([enti1,enti2rr])
        if entity == 'Institution':
            enti1 = enti1.drop('label',1)
            enti3 = pd.DataFrame(graph.run('MATCH (a:'+entity+') RETURN a.name,a.registered_name'),columns=[entity,'registered_name']).dropna()
            enti3 = enti3.groupby(entity)['registered_name'].agg(lambda x: ','.join(set(x))).reset_index()
            enti1 = pd.merge(enti1,enti3,on=entity,how='left')
        else:
            pass
    else:
        enti1 = pd.DataFrame(graph.run('MATCH (n:' + entity+') RETURN n.name'),
                              columns=[entity])
    return enti1

# 关联下的分布
def distri(ent1,ent2):
    df = relation1(ent1,ent2)
    df =df.groupby(ent1)[ent2].nunique().reset_index().rename(columns={ent2:ent2+'_Count'})
    df = df.sort_values(by=ent2+'_count',ascending=False)
    df.to_excel('./Outputs/'+ent1+'-'+ent2+'_Count.xlsx',index=False)
    return df


def excelsave():
    writer = pd.ExcelWriter('kbEntity.xlsx', engine='xlsxwriter')
    Insti = extract('Institution','y')
    Tech = extract('Technology','y')
    TF = extract('TechField','n')
    AF = extract('AiField', 'n')
    Ind = extract('Industry', 'n')
    frames = {'机构': Insti, '技术': Tech, '技术领域':TF,'智能领域':AF,'行业':Ind}
    for sheet, frame in frames.items():
        frame.to_excel(writer, sheet_name=sheet, index=False)
    writer.save()


def temp(ent):
    df = pureproperty(ent,'roles,round_scope,companySize,region,founded_at')
    df1 = relation1(ent,'AiField')
    df11 = df1.groupby(ent)['AiField'].apply(list).reset_index()
    df2 = relation1(ent,'TechField')
    df21 = df2[df2['TechField']=='自然语言处理']
    dff = pd.merge(df21,df,on=ent,how='left').drop('TechField',1)
    df22 = df2.groupby(ent)['TechField'].apply(list).reset_index()
    dff = pd.merge(dff,df22,on=ent,how='left')
    dff = pd.merge(dff,df11,on=ent,how='left')
    dff['founded_at'] = dff['founded_at'].apply(lambda x:timeadjust(x))
    return(dff)

if __name__ == '__main__':
    # pureproperty('Institution', 'roles,uuid')
    # relation1('Institution','Solution')
    temp('Institution').to_excel('自然语言处理领域机构.xlsx',index=False)



