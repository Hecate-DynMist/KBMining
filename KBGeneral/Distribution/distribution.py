from data import *

def strtolist(df,col,sym):
    df[col] = df[col].astype(str).apply(lambda x: x.lstrip('[').rstrip(']').strip().split(sym))
    return df

def listtorows(df,col):
    s = pd.DataFrame({col: np.concatenate(df[col].values)}, index=df.index.repeat(df[col].str.len()))
    dfs = s.join(df.drop(col, 1), how='outer')
    dfs.reset_index(drop=True, inplace=True)
    dfs[col] = dfs[col].apply(lambda x:x.replace("'", "").strip())
    return dfs

def dist(df,col1,col2,name):
    df = strtolist(df, col1, ',')
    df = listtorows(df,col1)
    df = strtolist(df, col2, ',')
    df = listtorows(df, col2)
    df = df.groupby(col1)[col1].count().reset_index(name=name)
    df = df.sort_values(by=name)
    return df

def dfmerge(df1,df2,df3,name):
    d1 = dist(df1,'供应商的智能领域','供应商UUID','AIOT创业公司')
    d2 = dist(df2,'解决方案的智能领域','解决方案UUID','解决方案')
    d3 = dist(df3,'案例应用的智能领域','案例UUID','客户案例')
    df = pd.concat([d1,d2,d3],1)
    df.to_excel('./Outputs/'+name+'.xlsx',index=False)

def dfmerge2(df1,df2,name):
    d1 = dist(df1,'案例应用的业务场景','案例UUID','客户案例')
    d2 = dist(df2,'解决方案的业务场景','解决方案UUID','解决方案')
    df = pd.concat([d1,d2],1)
    df.to_excel('./Outputs/' + name + '.xlsx', index=False)

# dfmerge(ps1,ps2,ps3,'公共服务智能领域分布')
# dfmerge2(ps4,ps5,'公共服务业务场景分布')
#
# dfmerge(pf1,pf2,pf3,'公共设施智能领域分布')
# dfmerge2(pf4,pf5,'公共设施业务场景分布')

# dfmerge(pb1,pb2,pb3,'公共智能领域分布')
# dfmerge2(pb4,pb5,'公共业务场景分布')

