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
win_test = 'rcjc'
engine = create_engine(f'mysql+pymysql://{win_user}:{win_password}@{win_host}:{win_port}/{win_test}', echo=True)

sql_v01 = "SELECT * FROM V01 "
# 通过pandas读取 机构数据
data_v01 = pd.read_sql(sql_v01, engine)
data_v01['INT_START_DT'] = pd.to_datetime(data_v01['INT_START_DT'], format="%Y/%m/%d")
data_v01['LAST_DUE_DT'] = pd.to_datetime(data_v01['LAST_DUE_DT'], format="%Y/%m/%d")
data_v01['ACTV_DT'] = pd.to_datetime(data_v01['ACTV_DT'], format="%Y/%m/%d")
data_v01['LAST_SETL_DT'] = pd.to_datetime(data_v01['LAST_SETL_DT'], format="%Y/%m/%d")
print(data_v01.info())
# data_v01['LOAN_TYP'] = \
data_v01['LOAN_TYP'].replace('马上贷消费贷款', '马上贷', inplace=True)
data_v01['LOAN_TYP'].replace('零押贷个人信用消费贷款', '零押贷', inplace=True)
data_v01['LOAN_TYP'].replace('零押贷(授信)', '零押贷', inplace=True)
data_v01['LOAN_TYP'].replace('组合贷（主动授信）', None, inplace=True)
# print(data_v01)
print(pd.crosstab(data_v01['LOAN_TYP'], data_v01['SETL_FLG'], normalize=True, margins=True))

gb_v01 = data_v01.groupby('LOAN_TYP')

print(gb_v01.describe().get('YKQX'))

data_rt = data_v01[data_v01['SETL_FLG'] == 'N']

gb_rt = data_rt.groupby('LOAN_TYP')
print(gb_rt.describe().get('EXCU_RATE'))
