import pandas as pd
import datetime

d1 = datetime.datetime.strptime('2012-04-01', '%Y-%m-%d')
d2 = datetime.datetime.strptime('2012-03-01', '%Y-%m-%d')
delta = d1 - d2
print(delta.days)
print(delta)