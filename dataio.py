import pandas as pd

def load_df():
    return pd.read_csv("data/compiled.csv", index_col=0, parse_dates=True)
