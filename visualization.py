import pandas as pd
import matplotlib.pyplot as plt

def plot_monthly(df, codigo):
    dfcod = df.groupby(['codigo', 'data']).sum().loc[codigo]
    dfmonth = dfcod.groupby(pd.Grouper(freq="M")).sum()

    dfmonth['qtde'].plot()


def rolling_mean(df, codigo, window=30):
    dfcod = df.groupby(['codigo', 'data']).sum().loc[codigo]
    dfcod = dfcod.resample("B").sum()
    dfr = dfcod['qtde'].rolling(window).mean()
    dfr.plot()
