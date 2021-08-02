import pandas as pd
import numpy as np
from sqlalchemy import create_engine


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


sql_cust = " SELECT * FROM V_LOAN_FSD_CUST "
data_cust = pd.read_sql(sql_cust, engine)

# print(data_cust_gp.describe())
data_cust['DUE_P'] = (data_cust['DUE_BASE']+data_cust['FYJ_BASE'])/data_cust['BASE_AMT']
data_cust_gp = data_cust.groupby('FH')
fh_cust_des = data_cust_gp.describe()

with pd.ExcelWriter('D:\\test\\fsd2-07.xlsx') as writer:
    data_cust.to_excel(writer, sheet_name='CUST', na_rep='0.00', float_format="%.4f")
    fh_cust_des.to_excel(writer, sheet_name='zh_describe', na_rep='0.00', float_format="%.4f")
