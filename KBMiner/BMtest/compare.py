import pandas as pd
patha = './Inputs/美国禁令分析/'
pathar = 'D:/Work/KB-Mining/Hecate/KBMiner/Outputs/'
## 美国禁令分析-技术词比较:compare(dfb,dfr,'项目技术词','kbM技术词','美国禁令-技术词比较.xlsx')
# def techtermadjust():
#     dfb = pd.read_excel(patha + '技术列表.xlsx')
#     def split(x):
#         if '|' in x:
#             return x.split('|')[1]
#         else:
#             return x
#     dfb['项目技术词'] = dfb['技术列表'].apply(lambda x:split(x))
#     dfb = dfb.drop('技术列表',1).drop_duplicates()
#     return dfb
# dfb = techtermadjust()
# dfr = pd.read_excel(pathar+'technologies.xlsx').rename(columns={'Key': 'kbM技术词'})

## 美国禁令分析-机构比较:compare(dfb,dfr,'项目机构','kbM机构','美国禁令-关联机构比较.xlsx')
# dfb = pd.read_excel(patha+'机构关联技术.xlsx')[['institution']].rename(columns={'institution': '项目机构'})
# dfr = pd.read_excel(pathar+'Tech-Institution.xlsx')[['Institution']].rename(columns={'Institution': 'kbM机构'})

## 美国禁令分析-解决方案比较:compare(dfb,dfr,'项目解决方案','kbM解决方案','美国禁令-关联解决方案比较.xlsx')
# dfb = pd.read_excel(patha+'解决方案关联技术.xlsx')[['Solution']].rename(columns={'Solution': '项目解决方案'})
# dfr = pd.read_excel(pathar+'Tech-Solution.xlsx')[['Solution']].rename(columns={'Solution': 'kbM解决方案'})

## 美国禁令分析-应用案例-解决方案-关联比较:compare(dfb,dfr,'项目二级关联机构','kbM二级关联机构','美国禁令-二级关联机构比较.xlsx')
# def dfbadjust(col):
#     dfb = pd.read_excel(patha+'技术案例所属的解决方案所直接关联的机构 .xlsx')[['Institution']].rename(columns={'Institution': '项目二级关联机构'})
#     dfb[col] = dfb[col].apply(lambda x:eval(x))
#     inlist=[]
#     for item in dfb[col]:
#         if str(item) != '[]':
#             for it in item:
#                 inlist.append(it)
#     dfbf = pd.DataFrame(inlist,columns=[col])
#     return dfbf
# dfb = dfbadjust('项目二级关联机构')
# dfr = pd.read_excel(pathar+'Tech-Institution.xlsx')[['Institution']].rename(columns={'Institution': 'kbM二级关联机构'})

def compare(dfb,dfr,colb,colr,filename):
    dfb = dfb.drop_duplicates()
    dfr = dfr.drop_duplicates()
    df = pd.merge(dfb,dfr,left_on=colb,right_on=colr,how='outer').sort_values(by=[colb,colr])
    writer = pd.ExcelWriter('./Outputs/'+filename,engine='xlsxwriter')
    df1 = df.dropna().drop_duplicates()
    df2 = df[df[colb].astype(str) == 'nan'][[colr]].reset_index(drop=True)
    df3 = df[df[colr].astype(str) == 'nan'][[colb]].reset_index(drop=True)
    df4 = pd.concat([df2, df3], axis=1).drop_duplicates()
    df5 = pd.DataFrame(
        {colb+'数目': [len(dfb)], colr+'数目': [len(dfr)], '相同数目': [len(df1)], '不同数目': len(df2) + len(df3),'覆盖率':[len(df1)/len(dfb)]})
    frames = {'相同列表': df1, '不同列表': df4, '对比统计': df5}
    for sheet, frame in frames.items():
        frame.to_excel(writer, sheet_name=sheet, index=False)
    writer.save()

compare(dfb,dfr,'项目二级关联机构','kbM二级关联机构','美国禁令-二级关联机构比较.xlsx')