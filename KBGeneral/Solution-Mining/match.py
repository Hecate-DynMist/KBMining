from data import *

def merge(df1,df2,col1,col2,type):
    dfm = pd.merge(df1,df2,how='left',left_on=col1,right_on=col2)
    dfm = dfm[dfm[col2].astype(str) != 'nan']
    dfm = dfm.groupby(type)[col1].apply(list).reset_index()
    return dfm

instai = instai[instai['索引类别'].astype(str)=='[AiField,Wiki]'].reset_index(drop=True)
instaim = merge(instai,aidx,'AIField','aidx','Institution')

instinm = merge(instin,iidx,'Industry','iidx','Institution')

# instis2 = instis2[instis2['categories'].astype(str).apply(lambda x:x.startswith('[Technology'))]
# instis = pd.concat([instis1,instis2])
# instism = merge(instis2,sidx,'applytask','sidx','Institution')

insti = pd.merge(instaim,instinm,on='Institution',how='outer')
insti.to_excel('./Outputs/Institution_Match.xlsx',index=False)

solai = solai[solai['Category'].astype(str)=='[AiField,Wiki]'].reset_index(drop=True)
solaim = merge(solai,aidx,'AIField','aidx','Solution')

solin = solinat[solinat['labels(b)'].astype(str).apply(lambda x:'Industry' in x)]
solinm = merge(solin,iidx,'Target','iidx','Solution')
solinm = solinm.rename(columns={'Target':'Industry'})

solat = solinat[solinat['labels(b)'].astype(str).apply(lambda x:'ApplyTask' in x)]
solse = solinat[solinat['labels(b)'].astype(str).apply(lambda x:'Scenario' in x)]
solatse = pd.concat([solat,solse])
solatsem = merge(solatse,sidx,'Target','sidx','Solution')
solatsem = solatsem.rename(columns={'Target':'Scenario'})

solse = solinst[solinst['Category'].astype(str).apply(lambda x:'Institution' in x)]
solse = solse.groupby('Solution')['Institution'].apply(list).reset_index()

sol1 = pd.merge(solaim,solinm,on='Solution',how='outer')
sol2 = pd.merge(sol1,solatsem,on='Solution',how='outer')
sol = pd.merge(sol2,solse,on='Solution',how='left')

sol.to_excel('./Outputs/Solution_Match.xlsx',index=False)