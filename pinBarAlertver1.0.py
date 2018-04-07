"""
title:pinBarAlert
version:1.0
developer:ji_ryoo
"""
#coding: UTF-8
import asyncio
import ccxt
import json
import requests
import pandas
import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.dates import date2num


"""
exchange = ccxt.bitflyer({
'apiKey': '#', #ご自身のものに変更ください
'secret': '#', #ご自身のものに変更ください
})




balance = exchange.fetch_balance()
balanceArragend = json.dumps(balance,indent=True)
print(balanceArragend)
print(exchange.fetch_balance()['total']['BTC'])
btcxfTicker = exchange.fetch_ticker("FX_BTC_JPY")
print(json.dumps(btcxfTicker,indent=True))

timest = exchange.fetch_ticker("FX_BTC_JPY")["timestamp"]
timest = timest - 5 * 3600000
candles = exchange.fetch_ohlcv(symbol="FX_BTC_JPY",timeframe='1h',since = timest)
print(candles)
print(json.dumps(exchange.has,indent=True))
"""


periods = ["300","3600","86400"]
query = {"periods":','.join(periods)}

#cryptowathのREST APIからohlc取得
res = json.loads(requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params=query).text)["result"]
clmList=["open","high","low","close"]#データフレームカラム定義
idxList=[]#データフレームインデックスリスト定義
for period in periods:
    ohlcs = pandas.DataFrame()
    print("period=" + period)
    row = res[period]
    length = len(row)

    for column in row[:length-101:-1]:
        column[0] = datetime.datetime.fromtimestamp(column[0])
        idxList.append(column[0])
        m = pandas.DataFrame([[column[1],column[2],column[3],column[4]]])
        ohlcs=ohlcs.append(m)
        ohlcs.index = idxList
    ohlcs.columns = clmList

    print(ohlcs)
    idxList.clear()
    # グラフにプロット

fig = plt.figure()
ax = plt.subplot()
xdate = [x.date() for x in ohlcs.index]
ohlc = np.vstack((date2num(xdate), ohlcs.values.T)).T
mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='g', colordown='r',alpha=0.5)
ax.grid()
ax.set_xlim(ohlcs.index[-1].date(), ohlcs.index[-0].date())
fig.autofmt_xdate()
plt.title("day ohlc BTCFX/JPY")
plt.show() # 画像表示
