from data import *
from match import insti,sol

def listcounttocol(df,colg,col):
    dfs = df.groupby([colg])[col].apply(list).reset_index()
    dfss = pd.concat([dfs.drop([col], axis=1), dfs[col].apply(lambda x: dict(collections.Counter(x))).apply(pd.Series)],axis=1)
    # dfss.to_excel('./Outputs/'+col+'score.xlsx',index=False)
    return dfss

aidxsco = listcounttocol(aidxsco,'key','aidx')
iidxsco = listcounttocol(iidxsco,'key','iidx')
sidxsco = listcounttocol(sidxsco,'key','sidx')

insti['Industry'] = insti['Industry'].apply(lambda d: d if isinstance(d, list) else [])
insti['AIField'] = insti['AIField'].apply(lambda d: d if isinstance(d, list) else [])
insti['Index'] = insti['AIField']+insti['Industry']
insti = insti[['Institution','Index']]

sol['Industry'] = sol['Industry'].apply(lambda d: d if isinstance(d, list) else [])
sol['AIField'] = sol['AIField'].apply(lambda d: d if isinstance(d, list) else [])
sol['Scenario'] = sol['Scenario'].apply(lambda d: d if isinstance(d, list) else [])
sol['Index'] = sol['AIField']+sol['Industry']+sol['Scenario']
sol = sol[['Solution','Index']]

iidxscoad = iidxsco.drop('key',1)
idx = pd.concat([aidxsco,iidxscoad],axis=1)

def enmatch(idxlist,idxsco):
    idxsco['valkey'] = ''
    idxsco['score'] = ''
    idxsco['dic'] = ''
    idxsco['enmatch'] = ''
    idxsco['cumscore']=''
    for i in range(len(idxsco)):
        idxsco['valkey'][i]=[]
        idxsco['score'][i] = []
        for col in idxsco.columns[1:-5]:
            if idxsco[col][i]>0:
                idxsco['valkey'][i].append(col)
                idxsco['score'][i].append(idxsco[col][i])
        idxsco['dic'][i]=dict(zip(idxsco['valkey'][i], idxsco['score'][i]))
        idxsco['enmatch'][i] = list(set(idxlist).intersection(set(idxsco['valkey'][i])))
        cumscore = 0
        for val in idxsco['enmatch'][i]:
            cumscore = cumscore + idxsco['dic'][i][val]
        idxsco['cumscore'][i] = cumscore
    idxcs = idxsco[['key','enmatch','cumscore']]
    return idxcs

def final(df,col):
    dff = pd.DataFrame()
    for i in range(len(df)):
        df1 = enmatch(df['Index'][i],idx)
        df1[col] = df[col][i]
        dff = dff.append(df1)
    return dff

calscore = final(insti,'Institution')
calscore = calscore[['Institution','key','enmatch','cumscore']]
calscore.to_excel('./Outputs/instical.xlsx',index=False)