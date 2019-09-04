import pandas as pd
from datetime import datetime, date, timedelta

def skipped_days(csv_file):
    df = pd.read_csv(csv_file)
    data_strs = sorted(df.data.unique())
    datas = set(data_strs)

    start_day = date(2015, 1, 1)
    today = date.today()
    
    while start_day < today:
        start_day_str = start_day.strftime("%Y-%m-%d")
        if start_day_str not in datas:
            wkdy = start_day.weekday()
            if wkdy < 5:
                print(start_day)
        start_day += timedelta(days=1)
