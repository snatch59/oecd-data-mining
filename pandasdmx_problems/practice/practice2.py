import pandas as pd

typeDict = {'Types': ['yearly', 'monthly', 'daily', 'hourly']}
aDict = {'AUS_Dep_Results A': [3.1, 4.6, 7.9, 8.4]}
a1Dict = {'AUS_With_Results A': [3.1, 4.6, 7.9, 8.4]}
bDict = {'AUS_Dep_Results B': [5.4, 9.3, 1.2, 6.6]}
b1Dict = {'AUS_With_Results B': [5.4, 9.3, 1.2, 6.6]}
cDict = {'HUN_Dep_Results A': [2.1, 3.6, 4.9, 5.4]}
c1Dict = {'HUN_With_Results A': [2.1, 3.6, 4.9, 5.4]}
dDict = {'HUN_Dep_Results B': [9.4, 8.3, 7.2, 1.6]}
d1Dict = {'HUN_With_Results B': [9.4, 8.3, 7.2, 1.6]}

# python 3.5 unpack
table = {**typeDict, **aDict, **a1Dict, **bDict, **b1Dict, **cDict, **c1Dict, **dDict, **d1Dict}
indx = list(typeDict.keys())[0]

df = pd.DataFrame(table)
df.set_index(indx, inplace=True)
df.columns = pd.MultiIndex.from_tuples([tuple(c.split('_')) for c in df.columns])
print(df)
df.to_csv('practice2.csv')

print('\n', 'completed ...')