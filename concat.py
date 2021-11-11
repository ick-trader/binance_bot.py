import pandas as pd

print('Processing')

df_1 = pd.read_excel('2018.xlsx')
df_2 = pd.read_excel('2019.xlsx')
df_3 = pd.read_excel('2020.xlsx')
df_4 = pd.read_excel('2021.xlsx')

df_2019 = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)

df_2019.to_excel('2018_2021.xlsx')

print('Success')