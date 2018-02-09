import pandas as pd

df = pd.read_csv('FFS_BRA_solution2_long.csv')

stack = df.stack()
sorted = df.sort_index()

all_cols_list = df.columns.values.tolist()
pivot = df.pivot_table(values=all_cols_list[1], index=all_cols_list[0], columns=all_cols_list[2:])

pass
