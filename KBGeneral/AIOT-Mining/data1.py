import pandas as pd
pd.set_option('display.max_columns', None)
df1 = pd.read_excel('./Inputs/【关键词匹配】新闻汇总-AIOT+地产+公共.xlsx')
df2 = pd.read_excel('./Inputs/【标签匹配】新闻汇总-AIOT+地产+公共.xlsx').rename(columns={'识别的标签':'识别的关键词','识别相关机构[jieba]':'相关机构[jieba]','识别相关机构[KB]':'相关机构[KB]'})
df = pd.concat([df1,df2])
df = df.drop_duplicates(subset='id')

dfe1 = pd.read_excel('./Inputs/【关键词匹配】新闻汇总-AIOT+地产+公共.xlsx', sheet_name='地产')
dfe2 = pd.read_excel('./Inputs/【标签匹配】新闻汇总-AIOT+地产+公共.xlsx', sheet_name='地产')
dfe = pd.concat([dfe1,dfe2])
dfd = dfe.drop_duplicates(subset='id')
dfp1 = pd.read_excel('./Inputs/【关键词匹配】新闻汇总-AIOT+地产+公共.xlsx', sheet_name='公共')
dfp2 = pd.read_excel('./Inputs/【标签匹配】新闻汇总-AIOT+地产+公共.xlsx', sheet_name='公共')
dfp = pd.concat([dfp1,dfp2])
dfp = dfp.drop_duplicates(subset='id')

ar = pd.read_csv('./Inputs/articles.csv')[['id','title','created_at']]
ei = pd.read_csv('./Inputs/eigen_sources.csv')[['id','title','published_at']].rename(columns={'published_at':'created_at'})
da = pd.read_csv('./Inputs/dailies.csv')[['id','title','created_at']]
news = pd.concat([ar,da,ei], sort=False)
news = news.drop_duplicates(subset=['id'])

tag = pd.read_csv('./Inputs/tags.csv')
tagging = pd.read_csv('./Inputs/taggings.csv')

tag1 = tag[tag['node_type'].astype(str) == 'Graph::TechField']
tag1 = tag1[['id', 'name']].rename(columns={'name': 'TechField', 'id': 'tag_id'})
tag2 = tag[tag['node_type'].astype(str) == 'Graph::Technology']
tag2 = tag2[['id', 'name']].rename(columns={'name': 'Technology', 'id': 'tag_id'})
tag = pd.concat([tag1,tag2])
tagging = tagging[['tag_id', 'taggable_id']]