"""
title:pinBarAlert
version:1.0
developer:ji_ryoo
"""
import asyncio
import ccxt
import json
import requests

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

res = json.loads(requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params=query).text)["result"]
for period in periods:
    print("period=" + period)
    row = res[period]
    length = len(row)
    for column in row[:length-20:-1]:
        print(column)