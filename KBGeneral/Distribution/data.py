import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
estate = pd.read_excel('./Inputs/estate.xlsx')
publics = pd.read_excel('./Inputs/publicserve.xlsx')
publicf = pd.read_excel('./Inputs/publicfacility.xlsx')
public = pd.concat([publics,publicf])

def extractcol(estate):
    edf1 = estate[['研究主题类别', '供应商UUID', '供应商的智能领域']]
    edf1 = edf1[edf1['研究主题类别'] == 'AIOT创业公司']
    edf2 = estate[['研究主题类别', '解决方案UUID', '解决方案的智能领域']]
    edf2 = edf2[edf2['研究主题类别'] == '行业解决方案']
    edf2 = edf2.dropna()
    edf3 = estate[['研究主题类别', '案例UUID', '案例应用的智能领域']]
    edf3 = edf3[edf3['研究主题类别'] == '智能化案例']
    edf3 = edf3.dropna()
    edf4 = estate[['研究主题类别', '案例UUID', '案例应用的业务场景']]
    edf4 = edf4[edf4['研究主题类别'] == '智能化案例']
    edf4 = edf4.dropna()
    edf5 = estate[['研究主题类别', '解决方案UUID', '解决方案的业务场景']]
    edf5 = edf5[edf5['研究主题类别'] == '行业解决方案']
    edf5 = edf5.dropna()
    return edf1,edf2,edf3,edf4,edf5

ps1,ps2,ps3,ps4,ps5 = extractcol(publics)
pf1,pf2,pf3,pf4,pf5 = extractcol(publicf)
pb1,pb2,pb3,pb4,pb5 = extractcol(public)
pb1 = pb1.drop_duplicates(subset='供应商UUID').dropna()
pb2 = pb2.drop_duplicates(subset='解决方案UUID').dropna()
pb3 = pb3.drop_duplicates(subset='案例UUID').dropna()
pb4 = pb4.drop_duplicates(subset='案例UUID')
pb5 = pb5.drop_duplicates(subset='解决方案UUID')

def origin():
    pb11 = pb1.rename(columns={'供应商UUID':'UUID','供应商的智能领域':'智能领域'})
    pb21 = pb2.rename(columns={'解决方案UUID':'UUID','解决方案的智能领域':'智能领域'})
    pb31 = pb3.rename(columns={'案例UUID':'UUID','案例应用的智能领域':'智能领域'})
    pb41 = pb4.rename(columns={'案例UUID':'UUID','案例应用的业务场景':'业务场景'})
    pb51 = pb5.rename(columns={'解决方案UUID':'UUID','解决方案的业务场景':'业务场景'})
    pd.concat([pb11,pb21,pb31]).to_excel('公共智能领域.xlsx',index=False)
    pd.concat([pb41,pb51]).to_excel('公共业务场景.xlsx',index=False)

# origin()








