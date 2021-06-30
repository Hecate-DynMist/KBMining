from data import inscmerge,soscmerge
import pandas as pd

def strtolist(df,col,sym):
    df[col] = df[col].astype(str).apply(lambda x: x.lstrip('[').rstrip(']').replace("'",'').strip().split(sym))
    return df

inscmerge['keyscore'] = inscmerge['keyscore'].astype(int)
inscmerge['enscore'] = inscmerge['enscore'].astype(int)
inscmerge['cumscore'] = inscmerge['cumscore'].astype(int)
soscmerge['skeyscore'] = soscmerge['skeyscore'].astype(int)
soscmerge['senscore'] = soscmerge['senscore'].astype(int)
soscmerge['scumscore'] = soscmerge['scumscore'].astype(int)
inscmerge = strtolist(inscmerge,'sematch',', ')
inscmerge = strtolist(inscmerge,'enmatch',', ')
inscmerge = strtolist(inscmerge,'sekey',', ')
soscmerge = strtolist(soscmerge,'ssematch',', ')
soscmerge = strtolist(soscmerge,'senmatch',', ')
soscmerge = strtolist(soscmerge,'skeyword',', ')
mer = pd.merge(inscmerge,soscmerge,on='Institution',how='left')
mer = mer.groupby('Institution').agg(sematch=('sematch','first'),keyscore=('keyscore','first'),sekey=('sekey','first'),enscore=('enscore','first'),enmatch=('enmatch','first')
                                     ,cumscore=('cumscore','first'),Solution=('Solution',list),ssematch=('ssematch','sum'),skeyscore=('skeyscore','sum')
                                     ,skeyword=('skeyword','sum'),senscore=('senscore','sum'),senmatch=('senmatch','sum'),scumscore=('scumscore','sum')).reset_index()

mer['keyscore'] = mer['keyscore'].add(mer['skeyscore'], fill_value=0)
mer['enscore'] = mer['enscore'].add(mer['senscore'], fill_value=0)
mer['cumscore'] = mer['cumscore'].add(mer['scumscore'], fill_value=0)
mer['sematch'] = mer['sematch'].apply(lambda d: d if isinstance(d, list) else [])
mer['enmatch'] = mer['enmatch'].apply(lambda d: d if isinstance(d, list) else [])
mer['ssematch'] = mer['ssematch'].apply(lambda d: d if isinstance(d, list) else [])
mer['senmatch'] = mer['senmatch'].apply(lambda d: d if isinstance(d, list) else [])
mer['skeyword'] = mer['skeyword'].apply(lambda d: d if isinstance(d, list) else [])
mer['sematch'] = mer['sematch']+mer['ssematch']
mer['enmatch'] = mer['enmatch']+mer['senmatch']
mer['sekey'] = mer['sekey']+mer['skeyword']



# mer = mer.groupby('Institution').agg(解决方案=('Solution',list),对应场景=('sematch','sum'),Keyword场景分=('keyscore','sum'), \
#                                      Keyword场景Source=('sekey','sum'),Entity场景分=('enscore','sum'),Entity场景Source=('enmatch','sum') \
#                                      ,对应场景总得分=('cumscore','sum')).reset_index()
mer = mer.rename(columns={'Solution':'解决方案','keyscore':'Keyword场景分','sematch':'对应场景','enmatch':'Entity场景Source','sekey':'Keyword场景Source',
                          'cumscore':'对应场景总得分','enscore':'Entity场景分','Institution':'机构'})
def removenan(set):
    if 'nan' in set:
        set = set.remove('nan')
    return set

mer['对应场景'] = mer['对应场景'].apply(set)
mer['Keyword场景Source'] = mer['Keyword场景Source'].apply(set).apply(lambda x:removenan(x))
mer['Entity场景Source'] = mer['Entity场景Source'].apply(set)
mer['解决方案'] = mer['解决方案'].astype(str).replace('[nan]','')
mer = mer.drop(['ssematch','skeyscore','skeyword','senscore','senmatch','scumscore'],1)
mer.to_excel('./Outputs/addscore.xlsx',index=False)



