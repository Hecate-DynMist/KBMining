from data1 import *

def add(df,name):
    new = news[['id','created_at']]
    dftime = pd.merge(df,new,on='id',how='left')
    df0 = pd.merge(tag, tagging, on='tag_id', how='left')
    df12 = df0.groupby('taggable_id').agg(技术领域=('TechField',lambda x: set(x)),相关技术主体=('Technology',lambda x: set(x))).reset_index()
    df21 = pd.merge(dftime, df12, left_on='id', right_on='taggable_id', how='left').drop('taggable_id',1)
    df21.to_excel('./Outputs/'+name+'.xlsx',index=False)

add(df,'AIOT')




