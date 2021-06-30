import pandas as pd
pd.set_option('display.max_columns', None)
import os
path = './Inputs/'
files = os.listdir(path)

ar = pd.read_csv(path+files[0],encoding='utf-8')[['id','title']]
da = pd.read_csv(path+files[1],encoding='utf-8')[['id','title','url']]
ei = pd.read_csv(path+files[2],encoding='utf-8')[['id','title','source_url']].rename(columns={'source_url':'url'})
key = pd.read_excel(path+files[3])
tagging = pd.read_csv(path+files[4],encoding='utf-8')
tag = pd.read_csv(path+files[5],encoding='utf-8')


ar['label'] = 'article'
da['label'] = 'daily'
ei['label'] = 'eigen'
news = pd.concat([ar,da,ei], sort=False)
news = news.drop_duplicates(subset=['id'])
tag = tag[tag['node_type'].astype(str)=='Graph::Institution']
tag = tag[['id','name']].rename(columns={'name':'institution','id':'tag_id'})
tagging = tagging[['tag_id','taggable_id']]

def news_insti():
    df1 = pd.merge(tag,tagging,on='tag_id',how='left')
    df2 = pd.merge(news,df1,left_on='id',right_on='taggable_id',how='left')
    return df2[['id','title','institution','url','label']]

news = news_insti()
# news_insti()