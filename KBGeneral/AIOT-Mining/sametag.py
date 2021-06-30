from data import *

def same(listA,listB):
    retA = [i for i in listA if i in listB]
    df = pd.DataFrame(retA,columns =['SameTag'])
    df.to_excel('./Outputs/sametag.xlsx',encoding='utf-8',index=False)

def findsame():
    listA = key['Keyword'].tolist()
    listB = tag['name'].tolist()
    same(listA,listB)

def house():
    new = news.dropna(subset=['title'])
    def strinc(str):
        df = new[new['title'].str.contains(str)].sort_values(by =['title','institution']).drop_duplicates(subset=['title'])
        df.to_excel('./Outputs/'+str+'.xlsx',encoding='utf-8',index=False)
    strinc('地产')
    strinc('公共')

def extract(text):
    list = key['Keyword'].tolist()
    return [''.join(word) for word in list if word in text]

def dicval(list):
    dic = dict(zip(key.Keyword, key.AIOT))
    return set([''.join(dic[k]) for k in dic.keys() if k in list])

def AIOT():
    news['keyword'] = news['title'].astype(str).apply(lambda x:extract(x))
    news['AIOT'] = news['keyword'].apply(lambda x:dicval(x))
    new1 = news[news['keyword'].astype(str)!='[]']
    new1.to_excel('./Outputs/AIOT.xlsx', encoding='utf-8', index=False)

AIOT()


