
from Theme import *
# 技术主题
# 主函数。根据技术词输出关联一级实体（机构，解决方案，案例)，其中index为检索参数，property为属性输出参数，out为关联输出参数
def tech2institution(index,property,out):
    param1 = index.split(',')
    df = pd.DataFrame()
    if 'summary' in param1:
        df1 = relevant('Institution', 'summary','n')
        df = df.append(df1,ignore_index=True)
    if 'desc' in param1:
        df2 = relevant('Institution', 'desc','n')
        df = df.append(df2,ignore_index=True)
    if 'advantage_tech' in param1:
        df3 = tech_entity('Institution','advantage_tech', 'n')
        df = df.append(df3,ignore_index=True)
    if 'additional_info' in param1:
        df4 = tech_entity('Institution','additional_info', 'n')
        df = df.append(df4,ignore_index=True)
    if 'indexed_by' in param1:
        df5 = tech_entity('Institution','indexed_by', 'n')
        df = df.append(df5,ignore_index=True)
    if 'Solution_summary' in param1:
        df6 = techrelate1('Solution', 'Institution', 'summary')
        df = df.append(df6, ignore_index=True)
    if 'Solution' in param1:
        df7 = techrelate1('Solution', 'Institution', 'kbTech')
        df = df.append(df7,ignore_index=True)
    if 'BusinessCase' in param1:
        df8 = techrelate1('BusinessCase', 'Institution', 'kbTech')
        df = df.append(df8,ignore_index=True)
    if 'BusinessCase-Solution' in param1:
        df9 = techrelate2('BusinessCase', 'Solution', 'Institution' ,'kbTech')
        df = df.append(df9,ignore_index=True)
    if out!='none':
        df = teinrelate1('Institution',out,df)
    if property != 'none':
        dfp = pureproperty('Institution',property)
        df = pd.merge(df,dfp,on='Institution',how='left')
    adjust(df,'./Outputs/Tech-Institution.xlsx')

def tech2solution(index,property,out):
    param1 = index.split(',')
    df = pd.DataFrame()
    if 'summary' in param1:
        df1 = relevant('Solution', 'summary','n')
        df = df.append(df1,ignore_index=True)
    if 'desc' in param1:
        df2 = relevant('Solution', 'desc','n')
        df = df.append(df2,ignore_index=True)
    if 'core_tech' in param1:
        df3 = tech_entity('Solution','core_tech', 'n')
        df = df.append(df3,ignore_index=True)
    if 'serves' in param1:
        df4 = tech_entity('Solution','serves', 'n')
        df = df.append(df4,ignore_index=True)
    if 'indexed_by' in param1:
        df5 = tech_entity('Solution','indexed_by', 'n')
        df = df.append(df5,ignore_index=True)
    if 'Institution_summary' in param1:
        df6 = techrelate1('Institution', 'Solution', 'summary')
        df = df.append(df6, ignore_index=True)
    if 'Institution' in param1:
        df7 = techrelate1('Institution', 'Solution', 'kbTech')
        df = df.append(df7,ignore_index=True)
    if 'BusinessCase' in param1:
        df8 = techrelate1('BusinessCase', 'Solution', 'kbTech')
        df = df.append(df8,ignore_index=True)
    if 'BusinessCase-Institution' in param1:
        df9 = techrelate2('BusinessCase', 'Institution', 'Solution' ,'kbTech')
        df = df.append(df9,ignore_index=True)
    if out!='none':
        df = teinrelate1('Solution',out,df)
    if property != 'none':
        dfp = pureproperty('Solution',property)
        df = pd.merge(df,dfp,on='Solution',how='left')
    adjust(df,'./Outputs/Tech-Solution.xlsx')

def tech2businesscase(index,property,out):
    param1 = index.split(',')
    df = pd.DataFrame()
    if 'additional_info' in param1:
        df1 = tech_entity('BusinessCase','additional_info', 'n')
        df = df.append(df1,ignore_index=True)
    if 'applies_to' in param1:
        df2 = tech_entity('BusinessCase','applies_to', 'n')
        df = df.append(df2,ignore_index=True)
    if 'core_tech' in param1:
        df3 = tech_entity('BusinessCase','serves', 'n')
        df = df.append(df3,ignore_index=True)
    if 'indexed_by' in param1:
        df4 = tech_entity('BusinessCase','indexed_by', 'n')
        df = df.append(df4,ignore_index=True)
    if 'Solution_summary' in param1:
        df5 = techrelate1('Solution', 'BusinessCase', 'summary')
        df = df.append(df5, ignore_index=True)
    if 'Institution_summary' in param1:
        df6 = techrelate1('Institution', 'BusinessCase', 'summary')
        df = df.append(df6, ignore_index=True)
    if 'Institution' in param1:
        df7 = techrelate1('Institution', 'BusinessCase', 'kbTech')
        df = df.append(df7,ignore_index=True)
    if 'Solution' in param1:
        df8 = techrelate1('Solution', 'BusinessCase', 'kbTech')
        df = df.append(df8,ignore_index=True)
    if 'Institution-Solution' in param1:
        df9 = techrelate2('Institution', 'Solution', 'BusinessCase','kbTech')
        df = df.append(df9,ignore_index=True)
    if 'Solution-Institution' in param1:
        df10 = techrelate2('Solution', 'Institution', 'BusinessCase' ,'kbTech')
        df = df.append(df10,ignore_index=True)
    if out!='none':
        df = teinrelate1('BusinessCase',out,df)
    if property != 'none':
        dfp = pureproperty('BusinessCase',property)
        df = pd.merge(df,dfp,on='BusinessCase',how='left')
    adjust(df,'./Outputs/Tech-BusinessCase.xlsx')

def tech2IndustryAifield():
    excel = './Outputs/Tech-Industry&AiField.xlsx'
    xls = pd.ExcelWriter(excel)
    def distri(enti):
        df = relation1('Technology', enti, 'none', 'no')
        df2 = pd.merge(df, techbase, how='inner', left_on='Technology', right_on='Key')
        df3 = df2[enti].value_counts().reset_index().rename(columns={'index':enti,enti:'Counts'})
        df3.to_excel(xls, sheet_name=enti+'-distribution', index=False)
    distri('Industry')
    distri('AiField')
    xls.save()
    xls.close()

def index2entity(index,indexname,entity,out):
    def revelantmerge(e,o):
        if (e in ['Institution', 'BusinessCase']) and (o == 'AiField'):
            df1 = relation1(e, 'AiField', 'none', 'n')
            df2 = relation2(e, 'Solution', 'AiField', 'n')[[e, 'AiField']]
            df3 = pd.concat([df1, df2])
            df3 = df3.groupby(e)['AiField'].apply(set).reset_index()
            dff = pd.merge(df, df3, on=e, how='left')
        else:
            df1 = relation1(e, o, 'none', 'n')
            df1 = df1.groupby(e)[o].apply(set).reset_index()
            dff = pd.merge(df, df1, on=e, how='left')
        return dff.drop(index,1)
    excel = './Outputs/'+index+'('+indexname+').xlsx'
    xls = pd.ExcelWriter(excel)
    ou = out.split(',')
    ent = entity.split(',')
    def enout(df,ou):
        for o in ou:
            df = pd.merge(df,revelantmerge(e,o),on=[e],how='left')
        return df
    for e in ent:
        df = relation1(e, index, indexname, 'n')
        df = df.groupby(e)[index].apply(set).reset_index()
        df = enout(df,ou)
        df.to_excel(xls,sheet_name=e,index=False)
    xls.save()
    xls.close()

if __name__ == '__main__':
    tech2institution('BusinessCase-Solution', 'none', 'none') # 主函数，根据需求修改为需要的检索参数和输出参数
    # tech2solution('summary,desc,serves,core_tech,indexed_by', 'none','none')
    # tech2businesscase('Solution', 'uuid', 'Solution,Institution,Industry,AiField,Scenario')
    # tech2IndustryAifield()
    # index2entity('Industry','地产,公共服务','Institution,Solution','TechField')
    # index2entity('TechField','物联网技术,深度学习','Institution,BusinessCase','AiField,Industry')
    # techexpand('y')

