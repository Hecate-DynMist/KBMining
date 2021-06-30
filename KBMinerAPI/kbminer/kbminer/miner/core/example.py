import pandas as pd
import sys

fullpath=sys.argv[1]
name=sys.argv[2]

df = pd.read_excel(str(fullpath))
df = df[['涉及技术']]
print(df)
df.to_excel('./miner/core/Output/out.xlsx',index=False)
