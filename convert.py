import pandas as pd

print('\nConverting CSV File to XLSX FIle')

cont_1 = [1,2,3,4,5,6,7,8,9]

for i in cont_1:
    readfile = pd.read_csv(f'ETHUSDT-1d-2018-0{i}.csv')
    readfile.to_excel(f'ETHUSDT-1d-2018-0{i}.xlsx' , 
    index= None, header = True , startcol=0, startrow=1)

cont_2 = [ 10,11,12 ]

for i in cont_2:
    readfile = pd.read_csv(f'ETHUSDT-1d-2018-{i}.csv')
    readfile.to_excel(f'ETHUSDT-1d-2018-{i}.xlsx' , 
    index= None, header = True, startcol=0, startrow=1)

print('Converting Excel File')

for i in cont_1:
    eth_df = pd.read_excel(f'ETHUSDT-1d-2018-0{i}.xlsx')
    eth_df.columns =['date', 'open_eth', 'high_eth', 'low_eth', 'close_eth','F','G','H','I','J','K','L']
    eth_df.set_index('date', inplace=True)
    eth_df.drop(['F','G','H','I','J','K','L'], axis = 1 , inplace = True)
    eth_df.index = pd.to_datetime(eth_df.index, unit='ms')
    eth_df.to_excel(f'ETHUSDT-1d-2018-0{i}.xlsx')

for i in cont_2:
    eth_df = pd.read_excel(f'ETHUSDT-1d-2018-{i}.xlsx')
    eth_df.columns =['date', 'open_eth', 'high_eth', 'low_eth', 'close_eth','F','G','H','I','J','K','L']
    eth_df.set_index('date', inplace=True)
    eth_df.drop(['F','G','H','I','J','K','L'], axis = 1 , inplace = True)
    eth_df.index = pd.to_datetime(eth_df.index, unit='ms')
    eth_df.to_excel(f'ETHUSDT-1d-2018-{i}.xlsx')

print('Concatenating')

df_1 = pd.read_excel('ETHUSDT-1d-2018-01.xlsx')
df_2 = pd.read_excel('ETHUSDT-1d-2018-02.xlsx')
df_3 = pd.read_excel('ETHUSDT-1d-2018-03.xlsx')
df_4 = pd.read_excel('ETHUSDT-1d-2018-04.xlsx')
df_5 = pd.read_excel('ETHUSDT-1d-2018-05.xlsx')
df_6 = pd.read_excel('ETHUSDT-1d-2018-06.xlsx')
df_7 = pd.read_excel('ETHUSDT-1d-2018-07.xlsx')
df_8 = pd.read_excel('ETHUSDT-1d-2018-08.xlsx')
df_9 = pd.read_excel('ETHUSDT-1d-2018-09.xlsx')
df_10 = pd.read_excel('ETHUSDT-1d-2018-10.xlsx')
df_11 = pd.read_excel('ETHUSDT-1d-2018-11.xlsx')
df_12 = pd.read_excel('ETHUSDT-1d-2018-12.xlsx')

df_2018 = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10,df_11,df_12], ignore_index=True)

df_2018.to_excel('2018.xlsx')

print('\nSuccess')