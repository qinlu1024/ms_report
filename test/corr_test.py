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
sql_data_1 = "SELECT T.INDIC_KEY,T.INDIC_NAME,T.STAT_DT,T.IND_VAL " \
             "FROM t09_rm_indic T WHERE 1=1 " \
             "AND T.CURR_CD = \'HRMB\' " \
             "AND T.PERIOD = \'M\' " \
             "AND T.INDIC_TYPE = \'3\' " \
             "AND T.INDIC_KEY =\'YS_JG_164\' " \
             "AND EXISTS(SELECT 1 FROM t09_gl_subj_month M WHERE T.ORG_NUM = M.OP_ORG_NUM) "
res_data_1 = pd.read_sql(sql_data_1, engine)
# pd_exp_fz_ys = pd.pivot_table(res_data_1, values='IND_VAL', index='ORG_NUM', columns='STAT_DT',
#                               aggfunc=np.sum, fill_value=0)
# pd_exp_fz_ys = pd_exp_fz_ys.reset_index()
print(res_data_1)
'''
pd_exp_fz_ys = pd.pivot_table(res_data_1, values='V', index='ORG_NUM', columns='STAT_DT',
                              aggfunc=np.sum, fill_value=0)
pd_exp_fz_ys = pd_exp_fz_ys.reset_index()
pd_exp_fz_ys.drop(['ORG_NUM'], axis=1, inplace=True)
# print(pd_exp_fz_ys.info)
pd_exp_fz_ys = pd_exp_fz_ys.corr()
pd_exp_fz_ys.to_excel("path_2021-02-28.xlsx", sheet_name="Sheet1")
# sns.pairplot(pd_exp_fz_ys)
# plt.show()
'''

sns.set_theme(style="darkgrid")
sns.displot(
    res_data_1, x='IND_VAL', col='STAT_DT'
)
plt.show()
