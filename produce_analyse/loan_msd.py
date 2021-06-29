from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


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
col_dict = {'ACTV_MON': '放款月份', 'BHDT_BCH_CDE': '放款分行', 'PRODUCT_TYP': '产品类型', 'LOAN_TYP': '贷款类型',
            'DIS_AMT': '放款金额', 'ACT_NBR': '放款笔数', 'INT_DUE_MON': '观察月份', 'RES_AMT': '本金余额',
            'ETL_DATE2': '观察月份', 'YQ': '逾期率', 'TRD_MON': '观察月份', 'AGE': '客户年龄'}

sql_v01 = "SELECT * FROM T_loan_s01_msd "
# 通过pandas读取 机构数据
data_v01 = pd.read_sql(sql_v01, engine)
data_v01['INT_START_DT'] = pd.to_datetime(data_v01['INT_START_DT'], format="%Y/%m/%d")
data_v01['LAST_DUE_DT'] = pd.to_datetime(data_v01['LAST_DUE_DT'], format="%Y/%m/%d")
data_v01['ACTV_DT'] = pd.to_datetime(data_v01['ACTV_DT'], format="%Y/%m/%d")
data_v01['LAST_SETL_DT'] = pd.to_datetime(data_v01['LAST_SETL_DT'], format="%Y/%m/%d")
print(data_v01.info())
data_v01['LOAN_TYP'].replace('马上贷', '马上贷消费贷款', inplace=True)

print(data_v01[['YKQX', 'FKQX', 'DIS_AMT', 'EXCU_RATE']].describe())

'''
sns.set_theme(style="darkgrid")
sns.displot(data_v01['YKQX'], kde=True)
sns.displot(data_v01['FKQX'], kde=True)
sns.displot(data_v01['DIS_AMT']/10000, kde=True)
plt.show()
'''
