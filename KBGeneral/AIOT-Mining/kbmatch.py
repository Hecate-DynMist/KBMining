from data2 import *
def extract(text):
    list = techterm['n.name'].tolist()
    return set([''.join(word) for word in list if word in text])

def extracttech(df,name):
    df['新闻相关技术提取'] = df['新闻标题'].astype(str).apply(lambda x: extract(x))
    df['技术领域'] = df['技术领域'].astype(str).apply(lambda x:x.replace('nan, ','').replace("{nan}","")).replace('nan','').replace(',nan','')
    df['相关技术主体'] = df['相关技术主体'].astype(str).apply(lambda x: x.replace('nan, ', '').replace("{nan}","")).replace('nan','')
    df['新闻相关技术提取'] = df['新闻相关技术提取'].astype(str).apply(lambda x: x.replace('set()', ''))
    df.to_excel('./Outputs/'+name+'.xlsx',index=False)

extracttech(dfe,'地产f')
extracttech(dfp,'公共f')
extracttech(dfe,'AIOTf')