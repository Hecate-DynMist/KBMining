
from config import *

# 扩展词源
def techexpand(out):
    techa = pd.DataFrame(graph.run('MATCH (n:Technology)<-[r:alias_of]-(b) RETURN n.name,b.name'),columns=['tech','alias']) # 提取有alias的技术词
    techna = pd.DataFrame(graph.run('MATCH (n:Technology) WHERE NOT (n)<-[:alias_of]-() AND NOT (n)-[:alias_of]->() Return n.name'),columns=['tech']) # 提取无alias的技术词
    tf = pd.DataFrame(graph.run('MATCH (n:TechField) RETURN n.name'),columns=['tech'])
    techna = pd.concat([techna,tf])
    techa['Key'] = techa['tech'].apply(lambda x:fullmatch(x))
    techa['Keya'] = techa['alias'].apply(lambda x: fullmatch(x))
    techa['Score'] = techa['Key'].apply(lambda x:score(base,'Key','Score',x))
    techa['Scorea'] = techa['Keya'].apply(lambda x: score(base, 'Key', 'Score', x))
    techa['Score'] = np.where(techa['Score'] == 0, techa['Scorea'], techa['Score'])
    techa['Scorea'] = np.where(techa['Scorea'] == 0, techa['Score'], techa['Scorea'])
    techa1 = techa[['tech','Score','Key']]
    techa2 = techa[['alias','Scorea','Keya']].rename(columns={'alias':'tech','Scorea':'Score','Keya':'Key'})
    techna['Key'] = techna['tech'].apply(lambda x:fullmatch(x))
    techna = techna[techna['Key'].astype(str)!='[]']
    techna['Score'] = techna['Key'].apply(lambda x:score(base,'Key','Score',x))
    base1 = base.rename(columns={'Key':'tech'})
    techbasen = pd.concat([base1,techa1,techa2,techna])
    techbasen = techbasen[techbasen['Score']!=0].drop_duplicates(subset=['tech'])
    if out == 'y':
        techbasen.to_excel('./Outputs/technologies.xlsx', index=False)
    return techbasen.rename(columns={'Key':'origin','tech':'Key'})

# 属性和优势技术的一级关联
def relation1(enti1,enti2,index,out):
    if index == 'none' or index=='kbTech':
        df = pd.DataFrame(graph.run('MATCH (a:'+enti1+')-[]-(c:' + enti2 + ') RETURN a.name,c.name'),columns=[enti1, enti2])
    else:
        indexa = index.split(',')
        df = pd.DataFrame()
        for i in indexa:
            df1 = pd.DataFrame(graph.run('MATCH (a:'+enti1+')-[]-(c:' + enti2 + ') where c.name="'+i+'" RETURN a.name,c.name'),columns=[enti1, enti2])
            df = df.append(df1,ignore_index=True)
    df = df.drop_duplicates()
    dfa = df.groupby(enti1)[enti2].apply(list).reset_index()
    if out == 'y':
        dfa.to_excel('./Outputs/'+enti1+'-'+ enti2 + '('+index+').xlsx', index=False)
    return df

# 实体描述关键词提取，返回与主题词相关的实体
def relesep(entity,index):
    prty = pd.DataFrame(graph.run('MATCH (a:'+entity+') RETURN a.name,a.'+index),columns=[entity,index])
    prty = prty[prty[entity].astype(str)!='名称暂未收录']
    prty[index+'_keyword'] = prty[index].apply(lambda x:fullmatch(x))
    ent = prty[prty[index+'_keyword'].astype(str) != '[]']
    ent[index+'_score'] = ent[index+'_keyword'].apply(lambda x:score(base,'Key','Score',x))
    ent = ent.rename(columns={index+'_keyword':'Key',index+'_score':'Score'})
    return ent[[entity,'Key','Score']]
def relevant(entity,index,out):
    if (index == 'summary') or (index=='desc'):
        ent = relesep(entity,index)
    else:
        ent = relation1('Technology', entity, 'none','no')
        ent = pd.merge(ent,techbase,how='inner',left_on='Technology',right_on='Key')
        ent = ent.groupby(entity).agg(Key=('Technology',lambda x:list(x)),Score=('Score','sum')).reset_index()
    if out == 'y':
        ent.to_excel('./Outputs/Relevant_'+entity+'(from '+index+').xlsx',index=False)
    return ent

# 基于机构-技术的直接关联匹配
def tech_entity(entity,path,out):
    if path == 'indexed_by':
        df = pd.DataFrame(graph.run('MATCH (a:'+entity+')-[r:'+path+']-(c:TechField) RETURN c.name,a.name'),columns=['Technology', entity])
    else:
        df = pd.DataFrame(graph.run('MATCH (a:Technology)-[r:'+path+']-(c:'+entity+') RETURN a.name,c.name'),columns=['Technology', entity])
    ent = pd.merge(df,techbase,how='inner',left_on='Technology',right_on='Key')
    ent = ent.groupby(entity).agg(Key=('Technology', lambda x:list(x)),
                                  Score=('Score', 'sum')).reset_index()
    if out == 'y':
        ent.to_excel('./Outputs/tech_'+entity+'_(from '+path+').xlsx',index=False)
    return ent


# 属性和优势技术的二级关联
def relation2(enti1,enti2,enti3,out):
    df = pd.DataFrame(graph.run('MATCH (a:'+enti1+')-[]-(b:' + enti2+')-[]-(c:' + enti3+') RETURN a.name,b.name,c.name'),columns=[enti1, enti2,enti3]).drop_duplicates()
    if out == 'y':
        df.to_excel('./Outputs/'+enti1+'-'+ enti2 +'-'+enti3+ '.xlsx', index=False)
    return df
# 合并函数
def entitymerge(df1,df2,key):
    df = pd.merge(df1,df2,on=key,how='left')
    return df

# 技术相关的一级关联
def techrelate1(ent1,ent2,index):
    df1 = relevant(ent1,index,'no')
    df2 = relation1(ent1,ent2,'none','no')
    df = entitymerge(df1,df2,ent1)
    df = df.groupby(ent2).agg({'Key':'sum','Score':'sum'}).reset_index()
    return df

# 技术相关的二级关联
def techrelate2(ent1,ent2,ent3,index):
    df1 = relevant(ent1,index,'no')
    df2 = relation2(ent1,ent2,ent3,'no')
    df = entitymerge(df1, df2, ent1)
    df = df.groupby(ent3).agg({'Key': 'sum', 'Score': 'sum'}).reset_index()
    return df


# 根据技术词输出机构的1级关联数据
def teinrelate1(entbase,ent,df):
    out = ent.split(',')
    def relevantmerge(df,outenti):
        df2 = relation1(entbase,outenti,'none','n')
        df3 = pd.merge(df,df2,on=entbase,how='inner')[[entbase,outenti]]
        df3 = df3[df3[outenti].astype(str)!='名称暂未收录']
        df3 = df3.groupby(entbase)[outenti].apply(set).reset_index()
        return df3
    for i in out:
        df = pd.merge(df,relevantmerge(df,i),on=entbase,how='left')
    return df

# 根据技术词输出机构的2级关联数据
def teinrelate2(enbase,ent1,ent2):
    df1 = teinrelate1(enbase,ent1,'n')
    df2 = relation1(ent1,ent2,'none','n')
    df = pd.merge(df1,df2,on=ent1,how='inner')
    df = df.groupby(enbase).agg(ent1=(ent1,lambda x:set(x)),ent2=(ent2,lambda x:set(x))).rename(columns={'ent1':ent1,'ent2':ent2}).reset_index()
    return df

# 实体特定属性
def pureproperty(enti,column):
    column1 = enti.split()+column.split(',')
    if enti == 'Institution':
        pty = pd.DataFrame(graph.run(
            'MATCH (a:Institution) RETURN a.uuid,a.name,a.summary,a.roles,a.core_tech,a.financing_round,a.founded_at'), \
                           columns=['uuid', 'Institution', 'summary', 'roles', 'core_tech', 'financing_round',
                                    'founded_at'])[column1]
    elif enti == 'Solution':
        pty = pd.DataFrame(graph.run('MATCH (a:Solution) RETURN a.uuid,a.name,a.summary,a.core_tech'),columns=['uuid','Solution','summary','core_tech'])[column1]
    elif enti == 'BusinessCase':
        pty = pd.DataFrame(graph.run('MATCH (a:BusinessCase) RETURN a.uuid,a.name,a.core_tech'),
                           columns=['uuid', 'BusinessCase', 'core_tech'])[column1]
    else:
        pty = pd.DataFrame()
    return pty


def adjust(df,excelpath):
    excel = excelpath
    xls = pd.ExcelWriter(excel)
    df = df[df.iloc[:, 0].astype(str)!='nan']
    df = df[df.iloc[:, 0].astype(str) != '名称暂未收录']
    def timeadjust(x):
        try:
            return datetime.fromtimestamp(x).strftime('%Y-%m-%d')
        except:
            return None
    if 'founded_at' in df.columns:
        df['founded_at'] = df['founded_at'].apply(lambda x:timeadjust(x))
    df.to_excel(xls,sheet_name='All',index=False)
    dfs =pd.concat([df,df['Key'].apply(lambda x: dict(collections.Counter(x))).apply(pd.Series)],axis=1)
    Key = [item for item in dfs.columns if item not in df.columns]
    for key in Key:
        dfss = dfs.dropna(subset=[key])[df.columns]
        dfss.to_excel(xls, sheet_name=f'{key}', index=False)
    xls.save()
    xls.close()











