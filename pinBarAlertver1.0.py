#coding: UTF-8
"""
title:pinBarAlert
version:1.0
developer:ji_ryoo
"""

import ccxt
import json
import requests
import pandas
import datetime
import os
import numpy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.dates import date2num
import twitter


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

def pinbarJudge(data):
    hakoLength = abs(data[1]-data[4])
    barLength = data[2]-data[3]

    if(data[1]>data[4]):#陰線の場合
        sitahige = data[4]-data[3]
        uehige = data[2]-data[1]
        if(sitahige > barLength*0.6):
            return True
        if(uehige > barLength*0.6):
            return True
        else:
            return False
    else:#陽線の場合
        uehige = data[2]-data[4]
        sitahige = data[1]-data[3]
        if(sitahige > barLength*0.6):
            return True
        if(uehige > barLength*0.6):
            return True
        else:
            return False


periods = ["300","3600","86400"]
query = {"periods":','.join(periods)}

#cryptowathのREST APIからohlc取得
res = json.loads(requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params=query,).text)["result"]
clmList=["open","high","low","close"]#データフレームカラム定義
idxList=[]#データフレームインデックスリスト定義
for period in periods:
    ohlcs = pandas.DataFrame()
    print("period=" + period)
    row = res[period]
    length = len(row)
    count=0
    for column in row[:length-100:-1]:
        column[0] = datetime.datetime.fromtimestamp(column[0])
        idxList.append(column[0])
        m = pandas.DataFrame([[column[1],column[2],column[3],column[4]]])
        ohlcs=ohlcs.append(m)

        if(pinbarJudge(column)==True and count==0):

             os.system("osascript -e 'display notification \"{0}:A pinbar appears now!{1}\"'".format(period,column[0]))
            #twi.PostUpdate("@lemyelaki "+period+": A pinbar appears now!")


        print(pinbarJudge(column))
        count = count+1
    ohlcs.index = idxList
    ohlcs.columns = clmList

    print(ohlcs)
    idxList.clear()
    # グラフにプロット

fig = plt.figure()
ax = plt.subplot()
xdate = [x.date() for x in ohlcs.index]
ohlc = np.vstack((date2num(xdate), ohlcs.values.T)).T
mpf.candlestick_ohlc(ax, ohlc, width=0.1, colorup='g', colordown='r',alpha=1)
ax.grid()
ax.set_xlim(ohlcs.index[-1].date(), ohlcs.index[-0].date())
fig.autofmt_xdate()
s = pandas.Series(ohlcs['close'])
sma25 = s.rolling(window=25).mean()
sma5 = s.rolling(window=5).mean()
plt.plot(ohlcs.index, sma5)
plt.plot(ohlcs.index, sma25)
x=[ohlcs.index[90].date(),ohlcs.index[9].date()]
y=[700000,1000000]
plt.plot(x,y)
plt.title("day ohlc BTCFX/JPY")
#plt.show() # 画像表示
