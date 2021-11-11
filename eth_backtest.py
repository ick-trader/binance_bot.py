import pandas as pd

# Leer Excel y Cantidad de Datos a procesar

eth_df = pd.read_excel('2018_2021.xlsx', index_col=0, parse_dates=True)

cant_datos = eth_df.index.size
num_datos = int(cant_datos)
print(f'\nCantidad de Datos : {cant_datos}')

# Calculo de eth_sma_2

eth_df['eth_sma_2'] = 0.0

for i in range(1,cant_datos,1):
    eth_df['eth_sma_2'][i] = (eth_df['close_eth'][i-1] + eth_df['close_eth'][i] ) / 2

# Calculo de eth_ema_2

n = 2                                       # ema de n periodos
a = 2 / ( n + 1 )

eth_df['eth_ema_2'] = 0.0
eth_df['eth_ema_2'][n-1] = eth_df['eth_sma_2'][n-1]

for i in range(n,cant_datos,1):
    eth_df['eth_ema_2'][i] = (a * (eth_df['close_eth'][i])) + ((1-a) * eth_df['eth_ema_2'][i-1])

# Calculo de eth_sma_22

eth_df['eth_sma_22'] = 0.0

for i in range(21,cant_datos,1):
    eth_df['eth_sma_22'][i] = eth_df.iloc[i-21:i+1, eth_df.columns.get_loc('close_eth')].mean()

# Calculo de eth_ema_22

n = 22                                       # ema de n periodos
a = 2 / ( n + 1 )

eth_df['eth_ema_22'] = 0.0
eth_df['eth_ema_22'][n-1] = eth_df['eth_sma_22'][n-1]

for i in range(n,cant_datos,1):
    eth_df['eth_ema_22'][i] = (a * (eth_df['close_eth'][i])) + ((1-a) * eth_df['eth_ema_22'][i-1])

# Calculo de eth_sma_100

eth_df['eth_sma_100'] = 0.0

for i in range(99,cant_datos,1):
    eth_df['eth_sma_100'][i] = eth_df.iloc[i-99:i+1, eth_df.columns.get_loc('close_eth')].mean()

# Calculo de eth_ema_100

n = 100                                       # ema de n periodos
a = 2 / ( n + 1 )

eth_df['eth_ema_100'] = 0.0
eth_df['eth_ema_100'][n-1] = eth_df['eth_sma_100'][n-1]

for i in range(n,cant_datos,1):
    eth_df['eth_ema_100'][i] = (a * (eth_df['close_eth'][i])) + ((1-a) * eth_df['eth_ema_100'][i-1])

# Crear Columnas del Sistema

eth_df['Position'] = ''           # Crear Columna con valor inicial 0
eth_df['PnL'] = 0.0               # Crear Columna con valor inicial 0
eth_df['Trade ROE %'] = 0.0
eth_df['Capital'] = 0.0
eth_df['PnL Acumulado'] = 0.0

# Crear Columnas del Sistema

eth_df['Position2'] = ''           # Crear Columna con valor inicial 0
eth_df['PnL2'] = 0.0               # Crear Columna con valor inicial 0
eth_df['Trade ROE2 %'] = 0.0
eth_df['Capital2'] = 0.0
eth_df['PnL Acumulado2'] = 0.0



step = 1
nTrades = 0                     # Contar cantidad de trades
capi = 1                     # Capital inicial
cap = capi                      # Variable para sacar el capital final
comision = 0.001             # Comision Binance en eth_eth en SPOT

# System Execution con Stop al 6 %

long_signal = False
close_signal = False
buy_order = False
palanca = 1
stop = float(-0.06/palanca)
stopped = False

for i in range(100,cant_datos,step): 
    long_signal = (buy_order == False) and (eth_df['eth_ema_22'][i]  <  eth_df['eth_ema_2'][i]) and (eth_df['eth_ema_22'][i-1]  >  eth_df['eth_ema_2'][i-1]) and (eth_df['close_eth'][i] >= eth_df['eth_ema_100'][i]) 
    close_signal = (buy_order == True) and (eth_df['eth_ema_22'][i] > eth_df['eth_ema_2'][i]) 

    if buy_order == True:    
        '''StopLoss'''                              
        if ((( eth_df['open_eth'][i] / long_entryPrice ) - 1 ) <= stop ):
            buy_order = False
            long_exitPrice = eth_df['open_eth'][i]
            cap *= (1-comision)
            eth_df['Position'][i] ="SL Open "
            pnl = (((long_exitPrice/long_entryPrice)-1) * entryCap)    
            eth_df['PnL'][i] = pnl
            cap += pnl
            eth_df['Capital'][i] = cap + pnl
            eth_df['Trade ROE %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado'][i] = (((cap / capi) -1) * 100)
            stopped = True

        elif ~stopped and ((( eth_df['low_eth'][i] / long_entryPrice ) - 1 ) <= stop ):
            buy_order = False
            long_exitPrice = eth_df['low_eth'][i]
            cap *= (1-comision)
            eth_df['Position'][i] = "SL Low"
            pnl = (((long_exitPrice/long_entryPrice)-1) * entryCap)    
            eth_df['PnL'][i] = pnl
            cap += pnl
            eth_df['Capital'][i] = cap + pnl
            eth_df['Trade ROE %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado'][i] = (((cap / capi) -1) * 100)
            stopped = True
  
        elif ~stopped and ((( eth_df['high_eth'][i] / long_entryPrice ) - 1 ) <= stop ) :
            buy_order = False
            long_exitPrice = eth_df['high_eth'][i]
            cap *= (1-comision)
            eth_df['Position'][i] = "SL High"
            pnl = (((long_exitPrice/long_entryPrice)-1) * entryCap)    
            eth_df['PnL'][i] = pnl
            cap += pnl
            eth_df['Capital'][i] = cap + pnl
            eth_df['Trade ROE %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado'][i] = (((cap / capi) -1) * 100)
            stopped = True


        elif ~stopped and ((( eth_df['close_eth'][i] / long_entryPrice ) - 1 ) <= stop ) :
            buy_order = False
            long_exitPrice = eth_df['close_eth'][i]
            cap *= (1-comision)
            eth_df['Position'][i] = "SL Close"
            pnl = (((long_exitPrice/long_entryPrice)-1) * entryCap)    
            eth_df['PnL'][i] = pnl
            cap += pnl
            eth_df['Capital'][i] = cap + pnl
            eth_df['Trade ROE %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado'][i] = (((cap / capi) -1) * 100)
            stopped = True


    
    if ~stopped:
        if long_signal:
            '''Open Long Trade'''
            buy_order = True
            long_entryPrice = eth_df['close_eth'][i]
            cap *= (1-comision) 
            entryCap = cap       
            nTrades += 1
            eth_df['Position'][i] = "Entry Long"
            eth_df['Capital'][i] = cap

        if close_signal:
            '''Close Long Trade'''
            buy_order = False
            long_exitPrice = eth_df['close_eth'][i]
            cap *= (1-comision)
            eth_df['Position'][i] = "Close Long"
            pnl = (((long_exitPrice/long_entryPrice)-1) * entryCap)    
            eth_df['PnL'][i] = pnl
            cap += pnl
            eth_df['Capital'][i] = cap + pnl
            eth_df['Trade ROE %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado'][i] = (((cap / capi) -1) * 100)

    stopped = False
# Calcular la Funding Fee

first_price = eth_df['close_eth'][0]
last_price = eth_df['close_eth'][num_datos-1]

hold_roe_eth = ( ( ( last_price / first_price ) -1) * 100 )
retorno = (((cap-capi) / capi) * 100)
usd_inicial = first_price
usd_final = cap * last_price
trade_hold = usd_final / usd_inicial

print(f'\n LONG SYSTEM')
print(f'\nBuy n Hold eth: {hold_roe_eth} %')
print(f'Rentabilidad del Sistema: {retorno} %')
print(f'Capital Final: {cap} eth')
print(f'System vs Hold: x {retorno / hold_roe_eth}')
print(f'Trade & Hold vs Trade System: x {(trade_hold) / ((retorno/100)+1)}')
print(f'Trade & Hold vs Buy & Hold: x {(trade_hold) / ((hold_roe_eth/100)+1)}')
print(f'USD Inicial: $ {first_price}')
print(f'USD Final: $ {usd_final}')
print(f'Capital Multiplicado x {trade_hold}')
print("nTrades: " + str(nTrades))
print("desde " + str(eth_df.index[0]) + " hasta " + str(eth_df.index[-1]))
print('\n')

step = 1
nTrades = 0                     # Contar cantidad de trades
capi = 1                     # Capital inicial
cap = capi                      # Variable para sacar el capital final
comision = 0.001             # Comision Binance en eth_eth en SPOT

short_signal = False
close_signal = False
sell_order = False
stop = float(0.06/palanca)
stopped = False

for i in range(100,cant_datos,step): 
    short_signal = (sell_order == False) and (eth_df['eth_ema_22'][i]  >  eth_df['eth_ema_2'][i]) and (eth_df['eth_ema_22'][i-1]  <  eth_df['eth_ema_2'][i-1]) and (eth_df['close_eth'][i] <= eth_df['eth_ema_100'][i]) 
    close_signal = (sell_order == True) and (eth_df['eth_ema_22'][i] < eth_df['eth_ema_2'][i]) 

    if sell_order == True:    
        '''StopLoss'''                              
        if ~stopped and ((( eth_df['open_eth'][i] / short_entryPrice ) - 1 ) >= stop):
            sell_order = False
            short_exitPrice = eth_df['open_eth'][i]
            cap *= (1-comision)
            eth_df['Position2'][i] ="SL Open "
            pnl = (((-short_exitPrice/short_entryPrice)+1) * entryCap)    
            eth_df['PnL2'][i] = pnl
            cap += pnl
            eth_df['Capital2'][i] = cap + pnl
            eth_df['Trade ROE2 %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado2'][i] = (((cap / capi) -1) * 100)
            stopped = True

        elif ~stopped and ((( eth_df['high_eth'][i] / short_entryPrice ) - 1 ) >= stop ) :
            sell_order = False
            short_exitPrice = eth_df['high_eth'][i]
            cap *= (1-comision)
            eth_df['Position2'][i] = "SL High"
            pnl = (((-short_exitPrice/short_entryPrice)+1) * entryCap)    
            eth_df['PnL2'][i] = pnl
            cap += pnl
            eth_df['Capital2'][i] = cap + pnl
            eth_df['Trade ROE2 %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado2'][i] = (((cap / capi) -1) * 100)
            stopped = True


        elif ~stopped and ((( eth_df['low_eth'][i] / short_entryPrice ) - 1 ) >= stop ):
            sell_order = False
            short_exitPrice = eth_df['low_eth'][i]
            cap *= (1-comision)
            eth_df['Position2'][i] = "SL Low"
            pnl = (((-short_exitPrice/short_entryPrice)+1) * entryCap)    
            eth_df['PnL2'][i] = pnl
            cap += pnl
            eth_df['Capital2'][i] = cap + pnl
            eth_df['Trade ROE2 %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado2'][i] = (((cap / capi) -1) * 100)
            stopped = True

        elif ~stopped and ((( eth_df['close_eth'][i] / short_entryPrice ) - 1 ) >= stop ) :
            sell_order = False
            short_exitPrice = eth_df['close_eth'][i]
            cap *= (1-comision)
            eth_df['Position2'][i] = "SL Close"
            pnl = (((-short_exitPrice/short_entryPrice)+1) * entryCap)    
            eth_df['PnL2'][i] = pnl
            cap += pnl
            eth_df['Capital2'][i] = cap + pnl
            eth_df['Trade ROE2 %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado2'][i] = (((cap / capi) -1) * 100)
            stopped = True


    
    if ~stopped:
        if short_signal:
            '''Open short Trade'''
            sell_order = True
            short_entryPrice = eth_df['close_eth'][i]
            cap *= (1-comision) 
            entryCap = cap       
            nTrades += 1
            eth_df['Position2'][i] = "Entry short"
            eth_df['Capital2'][i] = cap

        if close_signal:
            '''Close short Trade'''
            sell_order = False
            short_exitPrice = eth_df['close_eth'][i]
            cap *= (1-comision)
            eth_df['Position2'][i] = "Close short"
            pnl = (((-short_exitPrice/short_entryPrice)+1) * entryCap)    
            eth_df['PnL2'][i] = pnl
            cap += pnl
            eth_df['Capital2'][i] = cap + pnl
            eth_df['Trade ROE2 %'][i] = ((pnl / entryCap) * 100)
            eth_df['PnL Acumulado2'][i] = (((cap / capi) -1) * 100)

    stopped = False

# Calcular la Funding Fee

first_price = eth_df['close_eth'][0]
last_price = eth_df['close_eth'][num_datos-1]

hold_roe_eth = ( ( ( last_price / first_price ) -1) * 100 )
retorno = (((cap-capi) / capi) * 100)
usd_inicial = first_price
usd_final = cap * last_price
trade_hold = usd_final / usd_inicial

print(f'\n SHORT STSTEM')
print(f'\nBuy n Hold eth: {hold_roe_eth} %')
print(f'Rentabilidad del Sistema: {retorno} %')
print(f'Capital Final: {cap} eth')
print(f'System vs Hold: x {retorno / hold_roe_eth}')
print(f'Trade & Hold vs Trade System: x {(trade_hold) / ((retorno/100)+1)}')
print(f'Trade & Hold vs Buy & Hold: x {(trade_hold) / ((hold_roe_eth/100)+1)}')
print(f'USD Inicial: $ {first_price}')
print(f'USD Final: $ {usd_final}')
print(f'Capital Multiplicado x {trade_hold}')
print("nTrades: " + str(nTrades))
print("desde " + str(eth_df.index[0]) + " hasta " + str(eth_df.index[-1]))
print('\n')

eth_df.to_excel('2018_2021.xlsx')    




