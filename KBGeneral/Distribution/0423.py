import pandas as pd
df = pd.read_excel('./Inputs/【0422_V4_M】地产与公共行业AIOT数据汇总.xlsx').rename(columns={'供应商名称':'机构名称'})
# df1 = pd.read_excel('./Inputs/AIOT机构_0423.xlsx')
df2 = pd.read_excel('./Inputs/机构注册名称对照表.xlsx')
df21 = pd.read_excel('./Inputs/AIOT机构(注册名称)_0423v2.xlsx')
df3 = pd.read_excel('./Inputs/地产行业解决方案.xlsx').rename(columns={'供应商名称':'机构名称'})
df4 = pd.read_excel('./Inputs/公共行业解决方案.xlsx').rename(columns={'供应商名称':'机构名称'})
# df5 = pd.read_excel('./Inputs/公共行业解决方案（注册名）.xlsx')
df5 = pd.read_excel('./Inputs/地产行业解决方案（注册名）(1).xlsx')

df6 = pd.read_excel('./Inputs/附录1.AIOT技术领域创业新秀.xlsx')
df7 = pd.read_excel('./Inputs/附录2.地产行业解决方案（注册名）.xlsx')
df8 = pd.read_excel('./Inputs/附录3.公共行业解决方案（注册名）.xlsx')
print(df6.columns,df7.columns,df8.columns)

def colrep(df1,df2,d1,d2,origin,target):
    cols = list(df1.columns)
    df1['lower'] = df1[d1].fillna('None').str.lower()
    df2['lower'] = df2[d2].fillna('None').str.lower()
    df1 = df1.merge(df2,on='lower',how='left')
    df1[target] = df1[target].fillna(df1[origin])
    df1 = df1.drop(['lower',d1,origin],1)
    df1.rename(columns={target:origin},inplace=True)
    df1 = df1[cols]
    return df1

# df3 = colrep(df1,df2,'机构名称','供应商名称','机构名称','供应商注册名称')
def bulkcolrep():
    dfr = colrep(df,df2,'机构名称','供应商名称','机构名称','供应商注册名称')
    dfrr = colrep(dfr,df2,'客户/应用方名称','供应商名称','客户/应用方名称','供应商注册名称')
    dfrr = dfrr.rename(columns={'机构名称':'供应商名称'})
    print(dfrr.columns)
    dfrr.to_excel('./Outputs/【0422_V4_M】地产与公共行业AIOT数据汇总（名称替代）.xlsx',index=False)

def count(x):
    if str(x) == "['nan']":
        return 0
    else:
        return len(x)


def strtolistcount(df,col,sym):
    df[col] = df[col].astype(str).apply(lambda x: x.lstrip('[').rstrip(']').strip().replace("'",'').split(sym))
    df[col+'计数'] = df[col].apply(lambda x:count(x))
    df[col] = df[col].astype(str).apply(lambda x:x.replace("['nan']",''))
    df[col] = df[col].apply(lambda x: x.lstrip('[').rstrip(']').strip().replace("'", '').replace(',', '；'))
    return df

def mulcount(df,list,name):
    for it in list:
        df = strtolistcount(df,it,'；')
    df.to_excel('./Outputs/'+name+'计数.xlsx',index=False)

def adjust(dfss,list,name):
    for col in list:
        dfss[col] = dfss[col].astype(str).apply(lambda x: x.lstrip('[').rstrip(']').strip().replace("'", '').replace(',', '；').replace('nan',''))
    dfss.to_excel('./Outputs/'+name+'(格式调整).xlsx',index=False)

# mulcount(df5,['解决方案的智能领域','解决方案应用场景','供应商名称','供应商产业链角色','AIOT所处层级'],'地产行业解决方案（注册名）')

adjust(df6,['相关行业','智能领域','产业链角色'],'附录1.AIOT技术领域创业新秀')
adjust(df7,['解决方案的智能领域','解决方案应用场景','供应商名称','供应商产业链角色','AIOT所处层级'],'附录2.地产行业解决方案（注册名）')
adjust(df8,['解决方案的智能领域','解决方案应用场景','供应商名称','供应商产业链角色','AIOT所处层级'],'附录3.公共行业解决方案（注册名）')
