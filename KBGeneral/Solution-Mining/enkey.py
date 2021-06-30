from data import *

def mergecount(df,col):
    df['count'] = df['count'].astype(int)
    df1 = df.groupby([col,'scenario']).agg(keyword=('keyword',set),score=('count',sum)).reset_index()
    return df1

solkeyscore = mergecount(solkey,'Solution')
instikeyscore = mergecount(instkey,'Institution')
solkeyscore = pd.merge(solkeyscore,solinst,on='Solution',how='left')

solkeyscore.to_excel('./Outputs/solkeyscore.xlsx',index=False)
instikeyscore.to_excel('./Outputs/instikeyscore.xlsx',index=False)
