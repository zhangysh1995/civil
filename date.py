import datetime
import pandas as pd

start_date = datetime.date(2014,8,1)
end_date = datetime.date(2020,12,1)

date_range = pd.date_range(start_date, end_date)
# date_range = date_range[date_range.day==1]

print(date_range)