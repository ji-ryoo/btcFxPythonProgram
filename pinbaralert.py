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
import numpy as np
import twitter
import numpy


class Pinbar:
    periods = []
    query = {"periods":','.join(periods)}
    res = json.loads(requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params=query,).text)["result"]
    clmList=["open","high","low","close"]#データフレームカラム定義
    idxList=[]#データフレームインデックスリスト定義
    ohlcs = pandas.DataFrame()

    def __init__(self,sock):
        self.sock = str(sock)
        self.periods.append(self.sock)

        for period in self.periods:
            print("period=" + period)
            row = self.res[period]
            length = len(row)
            count=0
            for column in row[:length-101:-1]:
                column[0] = datetime.datetime.fromtimestamp(column[0])
                self.idxList.append(column[0])
                m = pandas.DataFrame([[column[1],column[2],column[3],column[4]]])
                self.ohlcs=self.ohlcs.append(m)
                count = count+1
            self.ohlcs.index = self.idxList
            self.ohlcs.columns = self.clmList
            self.idxList.clear()

    def printAllOhlcs(self):
        listed = self.ohlcs[1:2].values.tolist()
        print(listed[0])

    def pinbarJudge(self):
        data = self.ohlcs[1:2].values.tolist()[0]
        hakoLength = abs(data[0]-data[3])
        barLength = data[1]-data[2]

        if(data[0]>data[3]):#陰線の場合
            sitahige = data[3]-data[2]
            uehige = data[1]-data[0]
            if(sitahige > barLength*0.6):
                return True
            if(uehige > barLength*0.6):
                return True
            else:
                return False
        else:#陽線の場合
            uehige = data[1]-data[3]
            sitahige = data[0]-data[2]
            if(sitahige > barLength*0.6):
                return True
            if(uehige > barLength*0.6):
                return True
            else:
                return False
    def outJudgeTime(self):
        pinbarForJudge = self.ohlcs[1:2].index.strftime( '%Y-%m-%d %H:%M:%S' )[0]
        return pinbarForJudge
