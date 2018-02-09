import pandas as pd

typeDict = {'Types': ['yearly', 'monthly', 'daily', 'hourly']}
aDict = {'Results A': [3.1, 4.6, 7.9, 8.4]}
bDict = {'Results B': [5.4, 9.3, 1.2, 6.6]}

# python 3.5 unpack
d = {**typeDict, **aDict, **bDict}
indx = list(typeDict.keys())[0]

df = pd.DataFrame(d)
df.set_index(indx, inplace=True)
print(df)
# df.to_csv('practice.csv')

print('\n', 'completed ...')
