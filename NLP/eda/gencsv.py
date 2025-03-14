import pandas as pd
import numpy as np

df = pd.read_csv("/home/dhruv/Documents/BE proj/NLP/libreoffice.csv")

df=df[["Assignee","Summary"]]


valcnt = df['Assignee'].value_counts()


valcnt = valcnt[valcnt>19]

valcnt = valcnt[valcnt<=200]
print(valcnt)
print(len(valcnt))

to_include = valcnt.index
# print(to_include)
print('')
# print(finaldf)
print('')
df = df[df.Assignee.isin(to_include)]
print('')
print(df)
df['Assignee'].value_counts().plot.bar(figsize = (50,25))
df.to_csv('libretest.csv')

# finaldf=pd.read_csv('eda_libretest.csv')
# plt = finaldf['Assignee'].value_counts().plot.bar(figsize = (50,25))
