import pandas as pd
from data import solinst

solcal = pd.read_excel('./Outputs/solcal.xlsx')
instical = pd.read_excel('./Outputs/instical.xlsx')

solcal['cumscore'] = solcal['cumscore'].astype(int)
# solcal = solcal[solcal['cumscore']>0]
solcal = pd.merge(solcal,solinst,how='left',on='Solution')

instical['cumscore'] = instical['cumscore'].astype(int)
instical = instical[instical['cumscore']>0]


solcal.to_excel('./Outputs/solcal.xlsx',index=False)
instical.to_excel('./Outputs/instical_zerofree.xlsx',index=False)