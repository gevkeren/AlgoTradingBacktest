import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None
# import os
import yfinance as yf
# import datetime
# import csv
# from google.colab import files

# 2-30, Jumps of 1
# Moving_average_length = 9
#
# # 1.01 - 3, Jumps of 0.01
# Buy_trigger = 1.15
#
# # 0.5 - 0.99, Jumps of 0.01
# Sell_triger = 0.85
# RatioLB = 8
# Moving_average_ratio = 4
# Buy_ratio = 0.95
# Sell_ratio = 1
def create_df(moving_avg_len=9 ,
        Buy_trigger=1.15,
        Sell_trigger=0.85,
        RatioLB=8,
        moving_avg_ratio=4,
        Buy_ratio=0.95,
        Sell_ratio=1):

    ES = yf.Ticker('^GSPC')

    ES_df = pd.DataFrame(ES.history(start='2007-01-01', end='2018-01-01', interval="1d", auto_adjust=False))
    ES_df = ES_df.reset_index()
    ES_df['Date'] = pd.to_datetime(ES_df['Date'], unit='s')

    VIX = yf.Ticker('^VIX')

    VIX_df = pd.DataFrame(VIX.history(start='2007-01-01', end='2018-01-01', interval="1d", auto_adjust=False))
    VIX_df = VIX_df.reset_index()
    VIX_df['Date'] = pd.to_datetime(VIX_df['Date'], unit='s')

    # data 3
    VIX3M = yf.Ticker('^VIX3M')

    VIX3M = pd.DataFrame(VIX3M.history(start='2007-01-01', end='2018-01-01', interval="1d", auto_adjust=False))
    VIX3M = VIX3M.reset_index()
    VIX3M['Date'] = pd.to_datetime(VIX3M['Date'], unit='s')

    # data 4
    E_mini = yf.Ticker('ES=F')

    E_mini = pd.DataFrame(E_mini.history(start='2007-01-01', end='2018-01-01', interval="1d", auto_adjust=False))
    E_mini = E_mini.reset_index()
    E_mini['Date'] = pd.to_datetime(E_mini['Date'], unit='s')



    # drop manualy all values that in E_mini and not in US_bond
    E_mini = E_mini.drop(192)
    E_mini = E_mini.set_index('Date')
    E_mini = E_mini.reset_index()
    E_mini = E_mini.drop(216)
    E_mini = E_mini.set_index('Date')
    E_mini = E_mini.reset_index()
    E_mini = E_mini.drop(1811)
    E_mini = E_mini.set_index('Date')
    E_mini = E_mini.reset_index()
    E_mini = E_mini.drop(2506)
    E_mini = E_mini.set_index('Date')
    E_mini = E_mini.reset_index()
    # E_mini = E_mini.drop(3888)
    # E_mini = E_mini.set_index('Date')
    # E_mini = E_mini.reset_index()

    # data 5
    US_tres = yf.Ticker('ZB=F')

    US_tres = pd.DataFrame(US_tres.history(start='2007-01-01', end='2018-01-01', interval="1d", auto_adjust=False))
    US_tres = US_tres.reset_index()
    US_tres['Date'] = pd.to_datetime(US_tres['Date'], unit='s')
    US_tres = US_tres.drop(0)
    US_tres = US_tres.set_index('Date')
    US_tres = US_tres.reset_index()

    comission = 3

    ITVS = 0
    BondRatio = 0
    ESRatio = 0
    RR = 0
    RelativeRatio = 0

    ratio = VIX_df['Close'] / VIX3M['Close']
    ratio = pd.Series(ratio)  # convert ratio array to a pandas Series
    ITVS = ratio.rolling(window=moving_avg_len).mean()

    BondRatio = abs((US_tres['Close'] - US_tres['Close'].shift(+RatioLB)) / US_tres['Close'])
    US_tres['Close'].shift(1)

    ESRatio = abs((E_mini['Close'] - E_mini['Close'].shift(+RatioLB)) / E_mini['Close'])

    RR = BondRatio/ESRatio

    RR = pd.Series(RR)  # convert RR array to a pandas Series
    RelativeRatio = RR.rolling(window=moving_avg_ratio).mean()

    # funtion to determine missing dates
    found = False

    for i in range(1, len(RelativeRatio) - 1):
        if (E_mini['Date'][i] != US_tres['Date'][i] and (not (found))):
            print(E_mini['Date'][i])
            print(i)
            found = True

    E_mini['ITVS'] = ITVS
    E_mini['Signal'] = E_mini['Close'] * 0

    for i in range(1, len(E_mini['Signal'] - 1)):
        if (ITVS[i] < Sell_trigger or (RelativeRatio[i] < Buy_ratio)):
            E_mini['Signal'][i] = 1
        if (ITVS[i] > Buy_trigger or (RelativeRatio[i] > Sell_ratio)):
            E_mini['Signal'][i] = -1

    E_mini['P/L'] = E_mini['Close'] * 0

    entry_price = 0
    exit_price = 0

    for i in range(1, len(E_mini['Signal'] - 1)):
        if (E_mini['Signal'][i] != E_mini['Signal'][i - 1]):
            if (E_mini['Signal'][i] == -1 and (E_mini['Signal'][i - 1] != 0)):
                exit_price = E_mini['Close'][i]
                E_mini['P/L'][i] = exit_price - entry_price - (comission / 50)
            if (E_mini['Signal'][i] == 1 and (E_mini['Signal'][i - 1] != 0)):
                exit_price = E_mini['Close'][i]
                E_mini['P/L'][i] = -1 * (exit_price - entry_price) - (comission / 50)
            if (E_mini['Signal'][i] == 0):
                exit_price = E_mini['Close'][i]
                if (E_mini['Signal'][i - 1] == 1):
                    E_mini['P/L'][i] = exit_price - entry_price - (comission / 50)
                else:
                    E_mini['P/L'][i] = -1 * (exit_price - entry_price) - (comission / 50)
            entry_price = E_mini['Close'][i]

    E_mini['Capital'] = E_mini['P/L'] * 0 + 70000

    for i in range(1, len(E_mini['Signal'] - 1)):
        E_mini['Capital'][i] = E_mini['P/L'][i] * 50 + E_mini['Capital'][i - 1]

    maxDD = 0
    iVal = 0
    jVal = 0
    DD = 0

    for i in range(0, len(E_mini['Capital'])):
        bechmark = E_mini['Capital'][i]
        for j in range(i + 1, len(E_mini['Capital'])):
            if (E_mini['Capital'][j] > bechmark):
                break
            DD = (E_mini['Capital'][j] / E_mini['Capital'][i]) - 1
            DD = E_mini['Capital'][j] - E_mini['Capital'][i]
            if (DD < maxDD):
                maxDD = DD
                iVal = i
                jVal = j

    E_mini['Annual prec'] = E_mini['Close'] * 0
    i = 252
    while (i < len(E_mini['Annual prec'])):
        E_mini['Annual prec'][i] = (E_mini['Capital'][i] - E_mini['Capital'][i - 252]) / 70000
        i = i + 251

    E_mini['Annual prec'] = E_mini['Annual prec'].replace(0, np.NaN)
    annual_return = E_mini['Annual prec'].mean(axis=0, skipna=True)
    annual_std = E_mini['Annual prec'].std(axis=0, skipna=True)
    # print(annual_return)
    # print(annual_std)
    # print(E_mini['Annual prec'].dropna())

    sharpe = (annual_return - 0.03) / annual_std

    E_mini.drop(['Adj Close', 'Dividends', 'Stock Splits'], axis=1, inplace=True)

    return E_mini, sharpe
    # E_mini.to_csv('Results.csv', encoding='utf-8-sig')
    # files.download('Results.csv')
