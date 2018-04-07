#!/usr/bin/env python
import pandas as pd

df_sample =\
pd.DataFrame([["day1","day2","day1","day2","day1","day2"],
              ["A","B","A","B","C","C"],
              [100,150,200,150,100,50],
              [120,160,100,180,110,80]] ).T #とりあえず適当なデータを作ります

df_sample.columns = ["day_no","class","score1","score2"]  #カラム名を付ける
df_sample.index   = [11,12,13,14,15,16]  #インデックス名を付ける
print(df_sample)
df = pd.DataFrame({
        'A' : [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 7, 8, 9, 10],
        'B' : [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8]
    })


df = pd.DataFrame({
        'A' : [1],
        'B' : [1]
    })
print(df)
