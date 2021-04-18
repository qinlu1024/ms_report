import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.charts import Bar, Line, Scatter, Page, Pie, Timeline
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import matplotlib.pyplot as plt

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

# 贷款数据
sql_zc_1 = "SELECT T.ORG_NUM, T.IND_VAL/10000 IND_VAL FROM t09_rm_indic T " \
           "WHERE 1=1  AND T.INDIC_KEY = \'ZCFZ_A_113\' AND T.ORG_LEVEL = \'4\' " \
           "AND T.CURR_CD = \'HRMB\'  AND T.PERIOD = \'M\'  AND T.STAT_DT = \'2021-03-31\'  "
data_zc_1 = pd.read_sql(sql_zc_1, engine, index_col='ORG_NUM')

sql_fz_2 = "SELECT T.ORG_NUM, T.IND_VAL/10000 IND_VAL FROM t09_rm_indic T " \
           "WHERE 1=1  AND T.INDIC_KEY = \'ZCFZ_B_208\' AND T.ORG_LEVEL = \'4\' " \
           "AND T.CURR_CD = \'HRMB\'  AND T.PERIOD = \'M\'  AND T.STAT_DT = \'2021-03-31\'  "
data_fz_2 = pd.read_sql(sql_fz_2, engine, index_col='ORG_NUM')

sql_sr_3 = "SELECT T.ORG_NUM, T.IND_VAL/10000 IND_VAL FROM t09_rm_indic T " \
           "WHERE 1=1  AND T.INDIC_KEY = \'LR_A_103\' AND T.ORG_LEVEL = \'4\' " \
           "AND T.CURR_CD = \'HRMB\'  AND T.PERIOD = \'Q\'  AND T.STAT_DT = \'2021-03-31\'  "
data_sr_3 = pd.read_sql(sql_sr_3, engine, index_col='ORG_NUM')

sql_cb_4 = "SELECT T.ORG_NUM, T.IND_VAL IND_VAL FROM t09_rm_indic T " \
           "WHERE 1=1  AND T.INDIC_KEY = \'YS_JG_106\' AND T.ORG_LEVEL = \'4\' " \
           "AND T.CURR_CD = \'HRMB\'  AND T.PERIOD = \'Q\'  AND T.STAT_DT = \'2021-03-31\'  "
data_cb_4 = pd.read_sql(sql_cb_4, engine, index_col='ORG_NUM')

# data_zc_1.drop(['BSBK0001', 'BSBK0002', 'BSBKI001', 'BSBKG014', 'BSBK1101', 'BSBK0101'], axis=0, inplace=True)
# data_fz_2.drop(['BSBK0001', 'BSBK0002', 'BSBKI001', 'BSBK1101', 'BSBK0101'], axis=0, inplace=True)
# data_sr_3.drop(['BSBK0001', 'BSBK0002', 'BSBKI001', 'BSBKG014', 'BSBK1101', 'BSBK0101'], axis=0, inplace=True)
# data_cb_4.drop(['BSBK0001', 'BSBK0002', 'BSBKI001', 'BSBKG014', 'BSBK1101', 'BSBK0101'], axis=0, inplace=True)

plt.figure()
# data_zc_1['IND_VAL'].plot.hist(bins=50)
data_cb_4['IND_VAL'].plot.hist()
plt.show()
