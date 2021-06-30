from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pandas as pd
graph = Graph("bolt://localhost:7687", user="neo4j", password="lene1111")
inputpath = 'D:/Work/KB-Mining/Hecate/KBMiner/Outputs/Industry(地产,公共服务).xlsx'
f = pd.ExcelFile(inputpath)
dfr = pd.DataFrame()
for i in f.sheet_names:
    d = pd.read_excel(inputpath, sheet_name=i)
    dfr = pd.concat([dfr, d])

def rowtorows(df,col,sym):
    df1 = df.drop(col, axis=1).join(df[col].str.split(sym,expand=True).stack().reset_index(level=1,drop=True).rename(col)).reset_index(drop=True)
    df1[col] = df1[col].astype(str).apply(lambda x:x.strip())
    return df1

def tostring(df,col,sym1,sym2):
    df[col] = df[col].astype(str)
    df[col] = df[col].apply(lambda x:x.strip().lstrip(sym1).rstrip(sym2).strip())
    return df

def typetorow(df,col,sym1,sym2):
    df = df.tostring(df,col,sym1,sym2)
    df = rowtorows(df,col,',')
    return df

def compare(index,dfr,entity):
    ent = entity.split(',')
    def enmerge(dfr,en):
        df = pd.DataFrame(graph.run('MATCH (a:'+index+')-[]-(c:' + en + ') RETURN a.name,c.name'),columns=[index, en])
        df = df.groupby(index)[en].nunique().reset_index().rename(columns={en:en+'_KB_counts'})
        if '{' and '}' in dfr[index].iloc[0]:
            dfr = typetorow(dfr,index,'{','}')
        elif '[' and ']' in dfr[index].iloc[0]:
            dfr = typetorow(dfr, index, '[', ']')
        else:
            dfr = dfr
        dfr = dfr.groupby(index)[en].nunique().reset_index().rename(columns={en:en+'_Project_counts'})
        dfr[index] = dfr[index].apply(lambda x:x.replace("'",''))
        dff = pd.merge(dfr,df,on='Industry',how='left')
        return dff
    frames = [enmerge(dfr, en) for en in ent]
    dfs = [df.set_index([index]) for df in frames]
    dff = pd.concat(dfs,1).reset_index()
    dff.to_excel('./Outputs/kb与项目分布比较.xlsx',index=False)

compare('Industry',dfr,'Institution,Solution')