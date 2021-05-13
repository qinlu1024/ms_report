import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# 数据库配置：
# 用户名
db_user = 'root'
# 密码
db_password = '123456'
# IP地址
db_host = '127.0.0.1'
# 端口号
db_port = 3306
# 数据库
db_name = 'regular_monitoring'
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', echo=True)

# data
sql_data_1 = "SELECT V.STAT_DT, V.GL_ACCT, V.ORG_NUM, V.V FROM V_TEST_1 V WHERE V.STAT_DT = DATE(\'2021-03-31\')"
res_data_1 = pd.read_sql(sql_data_1, engine)

pd_exp_fz_ys = pd.pivot_table(res_data_1, values='V', index='ORG_NUM', columns='GL_ACCT',
                              aggfunc=np.sum, fill_value=0)
pd_exp_fz_ys = pd_exp_fz_ys.reset_index()
pd_exp_fz_ys.drop(['ORG_NUM'], axis=1, inplace=True)
# print(pd_exp_fz_ys.info)
pd_exp_fz_ys = pd_exp_fz_ys.corr()
pd_exp_fz_ys.to_excel("path_2021-03-31.xlsx", sheet_name="Sheet1")
# sns.pairplot(pd_exp_fz_ys)
# plt.show()
