import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_monthly(df, codigo):
    dfcod = df.groupby(['codigo', 'data']).sum().loc[codigo]
    dfmonth = dfcod.groupby(pd.Grouper(freq="M")).sum()

    dfmonth['qtde'].plot()
