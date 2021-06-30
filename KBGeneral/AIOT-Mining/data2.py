import pandas as pd

df = pd.read_excel('./Outputs/AIOT.xlsx')
dfp = pd.read_excel('./Outputs/公共.xlsx')
dfe = pd.read_excel('./Outputs/地产.xlsx')
techterm = pd.read_csv('./Inputs/technologies.csv')
techterm = techterm[techterm['n.name'].apply(lambda x:len(x)>2)]