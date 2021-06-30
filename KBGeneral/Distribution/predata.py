import pandas as pd
all = pd.read_excel('./Inputs/neat/all.xlsx').rename(columns={'解决方案的智能领域':'智能领域'})
insti = pd.read_csv('./Inputs/neat/Institution.csv')
inai = pd.read_csv('./Inputs/neat/in-aif.csv')
inai = inai.groupby('uuid')['AiField'].apply(list).reset_index()
institution = pd.merge(insti,inai,on='uuid',how='left')
instib = all[['供应商名称','供应商UUID','智能领域','供应商产业链角色']]
institution = institution.rename(columns={'uuid':'供应商UUID'})
def split(x):
    if not isinstance(x, float):
        x = x.replace("'",'').replace('[','').replace(']','')
    return list(set(x.split(',')))
instib['供应商产业链角色'] = instib['供应商产业链角色'].replace('未知','')

def update(up,kb,dropcol,name):
    up.dropna(subset=['智能领域'])
    up1 = up[up['uuid'].astype(str)=='nan']
    up2 = up[up['uuid'].astype(str) !='nan']
    kb1 = pd.merge(kb,up2,on='uuid',how='inner')
    kb1['AiField'] = kb1['AiField'].map(str)+kb1['智能领域'].map(str)
    kb1['AiField'] = kb1['AiField'].apply(lambda x:split(x))
    kb1 = kb1.drop_duplicates(subset='uuid').drop('智能领域',1).drop(dropcol,1)
    kb2 = pd.merge(kb, up2, on='uuid', how='left')
    kb2 = kb2[kb2['智能领域'].astype(str)!='nan'].drop('智能领域',1).drop(dropcol,1)
    kbf1 = pd.concat([kb1,kb2]).rename(columns={'AiField':'智能领域'})
    kbf = pd.concat([kbf1,up1])
    kbf.to_excel('./Outputs/'+name+'更新.xlsx', index=False)

def instiupdate():
    instib = instib.dropna(subset=['智能领域'])
    instib1 = instib[instib['供应商UUID'].astype(str)=='nan']
    instib2 = instib[instib['供应商UUID'].astype(str)!='nan']
    institution2 = pd.merge(institution,instib2,on='供应商UUID',how='inner')
    institution2['AiField'] = institution2['AiField'].map(str)+','+institution2['智能领域'].map(str)
    institution2['AiField'] = institution2['AiField'].apply(lambda x:split(x))
    institution2 = institution2.drop_duplicates(subset='供应商UUID').drop(['智能领域','供应商产业链角色','Institution'],1)
    institution3 = pd.merge(institution,instib2,on='供应商UUID',how='left')
    institution3 = institution3[institution3['智能领域'].astype(str)=='nan'].drop(['智能领域','供应商产业链角色','Institution'],1)
    instif0 = pd.concat([institution2,institution3]).rename(columns={'roles':'供应商产业链角色','AiField':'智能领域'})
    instif = pd.concat([instif0,instib1])
    instif.to_excel('./Outputs/机构更新.xlsx',index=False)


