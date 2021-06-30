import pandas as pd
from py2neo import Graph
from datetime import datetime
import numpy as np
graph = Graph("bolt://localhost:7687", user="neo4j", password="lene1111")  # 在此处修改为本地neo4j的端口，用户名和密码
prodata = pd.read_csv('./Inputs/pro_datasets_202008201428.csv').fillna('null')
proresearch = pd.read_csv('./Inputs/pro_researches_202008201428.csv').fillna('null')
dynamiclines = pd.read_csv('./Inputs/dynamiclines_202008201415.csv').fillna('null')
tagging = pd.read_csv('./Inputs/taggings_202008201428.csv')[['tag_id','taggable_type']].fillna('null')
tags = pd.read_csv('./Inputs/tags_202008201428.csv')[['id','name','node_type']]

def timeadjust(x):
    try:
        return datetime.fromtimestamp(x).strftime('%Y-%m-%d')
    except:
        return None

# 实体及其属性提取
def property(enti):
    if enti == 'Institution':
        pty = pd.DataFrame(graph.run(
            'MATCH (a:Institution) RETURN a.uuid,a.name,a.roles,a.round_scope,a.companySize,a.region,a.founded_at'), \
                           columns=['uuid', 'Institution', 'roles', 'round_scope', 'companySize', 'region',
                                    'founded_at'])
        pty['founded_at'] = pty['founded_at'].apply(lambda x:timeadjust(x))
    elif enti == 'Solution':
        pty = pd.DataFrame(graph.run('MATCH (a:Solution) RETURN a.uuid,a.name,a.region'),columns=['uuid','Solution'])
    else:
        pty = pd.DataFrame()
    return pty.fillna('null')

# 实体及其关联
def relation(ent1,ent2):
    df = pd.DataFrame(graph.run('MATCH (a:' + ent1 + ')-[]-(c:' + ent2 + ') RETURN a.name,c.name'), columns=[ent1, ent2])
    return df.fillna('null')

def listtorows(df,col):
    s = pd.DataFrame({col: np.concatenate(df[col].values)}, index=df.index.repeat(df[col].str.len()))
    dfs = s.join(df.drop(col, 1), how='outer')
    dfs.reset_index(drop=True, inplace=True)
    return dfs

def dist(ent1,ent2):
    df = relation(ent1, ent2)
    dff = df[ent2].value_counts().reset_index().rename(columns={'index': ent2, ent2: ent2 + '_count'})
    return dff

def distsql(df,col):
    df = df[col].value_counts().reset_index().rename(columns={'index':col,col:col+'_count'})
    return df

def kbInstitution():
    frame = []
    for r in ['AiField','TechField','Industry']:
        frame.append(dist('Institution',r))
    dfp = property('Institution')
    roles = dfp[['Institution','roles']]
    roles['roles'] = roles['roles'].apply(lambda x:x.replace('null','[]'))
    roles1 = roles[roles['roles'].astype(str)!='[]']
    roles2 = roles[roles['roles'].astype(str) == '[]']
    roles1['roles'] = roles1['roles'].apply(lambda x: eval(x))
    roles1 = listtorows(roles1,'roles')
    roles = pd.concat([roles1,roles2])
    frame.append(roles['roles'].value_counts().reset_index().rename(columns={'index':'roles','roles':'roles_count'}))
    for p in ['round_scope', 'companySize', 'region','founded_at']:
        frame.append(dfp[p].value_counts().reset_index().rename(columns={'index':p,p:p+'_count'}))
    df = pd.concat(frame,1)
    return df

def kbSolution():
    frame = []
    for r in ['AiField','TechField','Industry','ApplyFormat']:
        frame.append(dist('Solution',r))
    dfproduce = pd.DataFrame(graph.run('MATCH p=(b)-[r:produce]->(a:Solution) RETURN a.name,b.name'), columns=['Solution', 'Institution']).fillna('null')
    inre = property('Institution')[['Institution','region']]
    dfregion = pd.merge(dfproduce,inre,on='Institution',how='left')
    frame.append(distsql(dfregion,'region'))
    df = pd.concat(frame,1)
    return df


def pro(df,cols):
    frame = []
    for i in cols.split(','):
        frame.append(distsql(df,i))
    df = pd.concat(frame,1)
    return df

def tag():
    xls = pd.ExcelWriter('./Outputs/pro_tag.xlsx')
    df = tagging
    tagdata = df[df['taggable_type']=='Pro::Dataset']
    tagresearch = df[df['taggable_type']=='Pro::Research']
    tagdym = df[df['taggable_type']=='Dynamicline']
    def merge(df):
        return pd.merge(df, tags, left_on='tag_id', right_on='id', how='left').drop('id',1)
    merge(distsql(tagdata,'tag_id')).to_excel(xls,sheet_name='pro_datasets',index=False)
    merge(distsql(tagresearch, 'tag_id')).to_excel(xls, sheet_name='pro_researches', index=False)
    merge(distsql(tagdym, 'tag_id')).to_excel(xls, sheet_name='dynamiclines', index=False)
    xls.save()
    xls.close()

def rowtorows(df,col,sym):
    df1 = df.drop(col, axis=1).join(df[col].str.split(sym,expand=True).stack().reset_index(level=1,drop=True).rename(col)).reset_index(drop=True)
    df1[col] = df1[col].astype(str).apply(lambda x:x.strip())
    return df1

def miniadjust(df,col,sym):
    df = df[[col]]
    df[col] = df[col].apply(lambda x:x.replace('{}','null').lstrip('{').rstrip('}'))
    df = df.rename(columns = {col:col+'_sep'})
    dff = rowtorows(df,col+'_sep',sym)
    dff = distsql(dff, col+'_sep')
    return dff

def article():
    df1 = pd.read_csv('./Inputs/articles_explored.csv')[['explore_id', 'published_at']]
    df2 = pd.read_csv('./Inputs/setting_configurations_202008211207.csv')
    df2 = df2[-4:][['id', 'name']]
    df = pd.merge(df1, df2, left_on='explore_id', right_on='id', how='inner')
    dff1 = df['name'].value_counts().reset_index().rename(columns={'index': 'category', 'name': 'category_count'})
    dff2 = df['published_at'].value_counts().reset_index().rename(
        columns={'index': 'published_at', 'published_at': 'published_at_count'})
    dff = pd.concat([dff1, dff2], 1)
    return dff

def adjust():
    xls = pd.ExcelWriter('./Outputs/ProV2_distritubitons.xlsx')
    kbSolution().to_excel(xls, sheet_name='KB solution', index=False)
    kbInstitution().to_excel(xls,sheet_name='KB institution',index=False)
    prodatacols = 'source,uploaded_at,amount,numerical,content_type,size,summary,quantity'
    pd.concat([miniadjust(prodata,'summary','、'),pro(prodata,prodatacols)],1).to_excel(xls,sheet_name='pro_datasets',index=False)
    prosearchcols = 'research_type,uploaded_at,industries,category,chinese'
    pd.concat([miniadjust(proresearch,'industries','；'),pro(proresearch,prosearchcols)],1).to_excel(xls,sheet_name='pro_researches',index=False)
    dynamiclinescols = 'dynamic_types,published_at'
    pd.concat([miniadjust(dynamiclines,'dynamic_types',','),pro(dynamiclines,dynamiclinescols)],1).to_excel(xls,sheet_name='dynamiclines',index=False)
    article().to_excel(xls,sheet_name='articles_explored',index=False)
    xls.save()
    xls.close()

if __name__ == '__main__':
    kbSolution().to_excel('./Outputs/KBSolution(0927).xlsx',index=False)
    kbInstitution().to_excel('./Outputs/KBInstitution(0927).xlsx',index=False)
    # adjust()
    # tag()