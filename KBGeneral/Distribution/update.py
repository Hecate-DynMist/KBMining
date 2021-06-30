import pandas as pd
import numpy as np
insti = pd.read_excel('./Inputs/AIOT合并机构.xlsx')

def strtolist(df,col,sym):
    df[col] = df[col].astype(str).apply(lambda x: x.lstrip('[').rstrip(']').strip().split(sym))
    return df

def listtorows(df,col):
    s = pd.DataFrame({col: np.concatenate(df[col].values)}, index=df.index.repeat(df[col].str.len()))
    dfs = s.join(df.drop(col, 1), how='outer')
    dfs.reset_index(drop=True, inplace=True)
    dfs[col] = dfs[col].apply(lambda x:x.replace("'", "").strip())
    return dfs

def dist(df,col1,col2,col3):
    def rep(x):
        if not isinstance(x,float):
            return x.replace('；',',').replace(';',',')

    df[col2] = df[col2].apply(lambda x:rep(x))
    df[col1] = df[col1].apply(lambda x: rep(x))
    def ds(col):
        df1 = strtolist(df, col, ',')
        df1 = listtorows(df1,col)
        d1 = df1[col].value_counts().reset_index().rename(columns=({'index':col,col:col+'分布'}))
        return d1
    d1 = ds(col1)
    d2 = ds(col2)
    d3 = ds(col3)
    df = pd.concat([d1,d2,d3],1)
    df.to_excel('机构分布.xlsx',index=False)

# dist(insti,'智能领域','产业链角色','相关行业')

def disttemp(filename,col,name):
    kb = pd.read_csv('./Inputs/'+filename)
    df = kb[col].value_counts().reset_index().rename(columns=({'index':'行业',col:'行业分布'}))
    df.to_excel(name+'行业分布.xlsx',index=False)

disttemp('IOT Inst & industry.csv','c.name','IOT')