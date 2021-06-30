from catedf import *
index = pd.read_excel('./Inputs/index.xlsx')
aidx = index['aidx'].to_frame()
iidx = index['iidx'].to_frame()
sidx = index['sidx'].to_frame()

aidx = rowtorows(aidx,'aidx','，')
iidx = rowtorows(iidx,'iidx','，')
sidx = rowtorows(sidx,'sidx','，')

aidx = aidx.drop_duplicates()
iidx = iidx.drop_duplicates()
sidx = sidx.drop_duplicates()

instai = pd.read_csv('./Inputs/insti_aifield.csv')
instin = pd.read_csv('./Inputs/insti_indus.csv')
# instis1 = pd.read_csv('./Inputs/instis.csv')
# instis2 = pd.read_csv('./Inputs/instis2.csv')

solai = pd.read_csv('./Inputs/solai.csv')
solinat = pd.read_csv('./Inputs/solinat.csv')
solinst = pd.read_csv('./Inputs/solinst.csv')

idxscore = pd.read_excel('./Inputs/level1.xlsx')
aidxsco = idxscore[['key','aidx']]
aidxsco = rowtorows(aidxsco,'aidx','，')
iidxsco = idxscore[['key','iidx']]
iidxsco = rowtorows(iidxsco,'iidx','，')
sidxsco = idxscore[['key','sidx']]
sidxsco = rowtorows(sidxsco,'sidx','，')

instkey = pd.read_excel('./Inputs/insti_key.xlsx')
solkey = pd.read_excel('./Inputs/sol_key.xlsx')

inscmerge = pd.read_excel('./Inputs/inscmerge.xlsx')
soscmerge = pd.read_excel('./Inputs/soscmerge.xlsx')
soscmerge = soscmerge[soscmerge['Solution']!='名称暂未收录']