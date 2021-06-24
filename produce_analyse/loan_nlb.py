from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# 数据库用户名
win_user = 'root'
# 数据库密码
win_password = '123456'
# 数据库ip地址
win_host = '127.0.0.1'
# 端口号
win_port = 3306
# 数据库
win_test = 'loan'
engine = create_engine(f'mysql+pymysql://{win_user}:{win_password}@{win_host}:{win_port}/{win_test}', echo=True)

sql_v01 = "SELECT * FROM v_loan_s01_nlb "
# 通过pandas读取 机构数据
data_v01 = pd.read_sql(sql_v01, engine)
data_v01['INT_START_DT'] = pd.to_datetime(data_v01['INT_START_DT'], format="%Y/%m/%d")
data_v01['LAST_DUE_DT'] = pd.to_datetime(data_v01['LAST_DUE_DT'], format="%Y/%m/%d")
data_v01['ACTV_DT'] = pd.to_datetime(data_v01['ACTV_DT'], format="%Y/%m/%d")
data_v01['LAST_SETL_DT'] = pd.to_datetime(data_v01['LAST_SETL_DT'], format="%Y/%m/%d")
print(data_v01.info())
