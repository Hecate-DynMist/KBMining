import pandas as pd

base = pd.read_excel('./Inputs/【0422_V4】AIoT项目数据汇总_Mos(1).xlsx') \
    .rename(columns={'研究主体类别':'研究主体','解决方案的智能领域':'智能领域','供应商名称':'机构名称','适用行业':'相关行业','供应商产业链角色':'产业链角色','供应商UUID':'机构UUID'})
bc = pd.read_excel('./Inputs/分析一[合并].xlsx',sheet_name='案例')
sol = pd.read_excel('./Inputs/分析一[合并].xlsx',sheet_name='解决方案')
insti = pd.read_excel('./Inputs/分析一[合并].xlsx',sheet_name='机构')


print(base.columns,bc.columns,sol.columns,insti.columns)

baseb = base[['研究主体', '案例名称', '相关行业', '智能领域', '案例UUID']]
bases = base[['研究主体', '解决方案名称', '相关行业', '智能领域', '解决方案UUID']]
basei = base[['研究主体', '机构名称', '相关行业', '智能领域', '产业链角色', '机构UUID']]

def uuiddiff(A,B):
    retD = list(set(B).difference(set(A)))
    return retD

def merge(basea,entity,uuid,name):
    basea1 = basea[basea[uuid].astype(str)=='nan']
    basea2 = basea[basea[uuid].astype(str)!='nan']
    B = basea2[uuid].to_list()
    A = entity[uuid].to_list()
    retD = uuiddiff(A,B)
    basea3 = basea2[basea2[uuid].isin(retD)]
    df = pd.concat([entity,basea1,basea3])
    df['研究主体'] = name
    df.to_excel('./Outputs/'+name+'.xlsx',index=False)

merge(baseb,bc,'案例UUID','案例')
merge(bases,sol,'解决方案UUID','解决方案')
merge(basei,insti,'机构UUID','机构')