import pandas as pd
import ast
import collections

estate = pd.read_excel('./Inputs/Inputs1/AIOTf.xlsx')
public = pd.read_excel('./Inputs/Inputs1/公共f.xlsx')

def init(df):
    df['date']=pd.to_datetime(df['created_at'])
    df['date'] = df['date'].map(lambda x: x.strftime('%Y-%m'))
    df = df[(df['date'] >= '2018-01') & (df['date'] <= '2020-03')]
    return df

estate = init(estate)
public = init(public)
public['技术领域'] = public['技术领域'].astype(str).apply(lambda x:x.replace(', nan',''))



def count(df,name):
    df1 = df.groupby(df['date'])['新闻标题'].count().reset_index(name=name)
    df1.to_excel('./Outputs/distOut/'+name+'.xlsx',index=False)

# count(estate,'地产数目统计')
# count(public,'公共数目统计')
def listcounttocol(df,colg,col):
    dfs = df.groupby([colg]).agg({col: sum}).reset_index()
    dfss = pd.concat([dfs.drop([col], axis=1), dfs[col].apply(lambda x: dict(collections.Counter(x))).apply(pd.Series)],axis=1)
    return dfss

def tfcount(df,name):
    df = df.dropna(subset=['技术领域'])
    df = df[df['技术领域'].astype(str)!='nan']
    df['技术领域'] = df['技术领域'].apply(lambda x:ast.literal_eval(x))
    df['技术领域'] = df['技术领域'].apply(list)
    df1 = listcounttocol(df,'date','技术领域')
    df1.to_excel('./Outputs/distOut/'+name+'.xlsx',index=False)

def techtodic(df,col):
    df1 = df.dropna(subset=[col])
    df1 = df1[df1[col].astype(str)!='nan']
    df1 = df1.reset_index(drop=True)
    df1 = df1.rename(columns={col:'技术词汇'})
    for i in range(len(df1['技术词汇'])):
        try:
            df1['技术词汇'][i] = ast.literal_eval(df1['技术词汇'][i])
        except:
            print(i,df['技术词汇'][i])
    return df1

def listcounttocoltop(df,colg,col):
    dfs = df.groupby(df[colg].dt.to_period('Q')).agg({col: sum}).reset_index()
    dfss = pd.concat([dfs.drop([col], axis=1), dfs[col].apply(lambda x: dict(collections.Counter(x).most_common(50))).apply(pd.Series)],axis=1)
    return dfss

def top50(df,name):
    df1 = techtodic(df,'相关技术主体')
    df2 = techtodic(df,'新闻相关技术提取')
    dfm = pd.concat([df1,df2])
    dfm['date'] = pd.to_datetime(dfm['date'])
    dfm['技术词汇'] = dfm['技术词汇'].apply(list)
    g = listcounttocoltop(dfm,'date','技术词汇')
    # g = dfm.groupby(dfm['date'].dt.to_period('Q'))['技术词汇'].sum().reset_index(name='技术词汇')
    # g['top 50'] = g['技术词汇'].apply(lambda x:collections.Counter(x).most_common(50))
    # g['top 50'] = g['top 50'].apply(lambda x:dict(x)).apply(pd.Series)
    g.to_excel('./Outputs/distOut/'+name+'.xlsx',index=False)
top50(public,'公共top50技术词')

# top50(estate,'地产top50技术词')






