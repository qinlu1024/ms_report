import pandas as pd
import numpy as np

data1 = {
    "a": [1, 2],
    "b": [3, 4]
}
data2 = {
    "c":[11,22],
    "d":[33,44],
    "e":[55,66]
}

df1 = pd.DataFrame(data1)
print(df1)
df2 = pd.DataFrame(data2)
print(df2)
df1['value']=1
df2['value']=1

df3 = df1.merge(df2, how='left', on='value')
print(df3)
del df3['value']
print(df3)
