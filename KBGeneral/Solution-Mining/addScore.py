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



# mer = mer.groupby('Institution').agg(????????????=('Solution',list),????????????=('sematch','sum'),Keyword?????????=('keyscore','sum'), \
#                                      Keyword??????Source=('sekey','sum'),Entity?????????=('enscore','sum'),Entity??????Source=('enmatch','sum') \
#                                      ,?????????????????????=('cumscore','sum')).reset_index()
mer = mer.rename(columns={'Solution':'????????????','keyscore':'Keyword?????????','sematch':'????????????','enmatch':'Entity??????Source','sekey':'Keyword??????Source',
                          'cumscore':'?????????????????????','enscore':'Entity?????????','Institution':'??????'})
def removenan(set):
    if 'nan' in set:
        set = set.remove('nan')
    return set

mer['????????????'] = mer['????????????'].apply(set)
mer['Keyword??????Source'] = mer['Keyword??????Source'].apply(set).apply(lambda x:removenan(x))
mer['Entity??????Source'] = mer['Entity??????Source'].apply(set)
mer['????????????'] = mer['????????????'].astype(str).replace('[nan]','')
mer = mer.drop(['ssematch','skeyscore','skeyword','senscore','senmatch','scumscore'],1)
mer.to_excel('./Outputs/addscore.xlsx',index=False)



