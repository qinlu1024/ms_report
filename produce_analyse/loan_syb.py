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

sql_v01 = "SELECT * FROM T_loan_s01_syb2 "
# 通过pandas读取 机构数据
data_v01 = pd.read_sql(sql_v01, engine)
data_v01['INT_START_DT'] = pd.to_datetime(data_v01['INT_START_DT'], format="%Y/%m/%d")
data_v01['LAST_DUE_DT'] = pd.to_datetime(data_v01['LAST_DUE_DT'], format="%Y/%m/%d")
data_v01['ACTV_DT'] = pd.to_datetime(data_v01['ACTV_DT'], format="%Y/%m/%d")
data_v01['LAST_SETL_DT'] = pd.to_datetime(data_v01['LAST_SETL_DT'], format="%Y/%m/%d")
print(data_v01.info())

data_v01['PARTNER_TP'] = data_v01['PARTNER_NO'].apply(lambda x: x[0])
gb_cust_tp = data_v01.groupby('PARTNER_TP')
gb_hk = data_v01.groupby('REP_CATE')
data_hk = gb_hk.describe()
des_data_v01 = gb_cust_tp.describe()
print(des_data_v01.sum())
data_amt = pd.pivot_table(data_v01, values='DIS_AMT', index='LOAN_SEC_TYP', columns='PARTNER_TP',
                          aggfunc=np.sum, margins=True)
data_amt2 = pd.pivot_table(data_v01, values='DIS_AMT', index='LOAN_SEC_TYP', columns='PARTNER_TP',
                           aggfunc=np.count_nonzero, margins=True)
data_amt3 = pd.pivot_table(data_v01, values='DIS_AMT', index=['REP_CATE'], columns='PARTNER_TP',
                           aggfunc=np.sum, margins=True)
data_amt4 = pd.pivot_table(data_v01, values='DIS_AMT', index=['REP_CATE'], columns='LOAN_CLASS',
                           aggfunc=[np.sum, np.count_nonzero], margins=True)
data_amt5 = pd.pivot_table(data_v01, values='DIS_AMT', index=['REP_CATE'], columns='LOAN_CLASS',
                           aggfunc=np.count_nonzero, margins=True)
data_diyu = pd.pivot_table(data_v01, values='DIS_AMT', index=['province_name'],
                           aggfunc=[np.sum, np.count_nonzero], margins=True)
data_age = data_v01['AGE'].describe()

# 生成数据报表
with pd.ExcelWriter('D:\\test\\syb13.xlsx') as writer:
    des_data_v01.to_excel(writer, sheet_name='describe', na_rep='0.00', float_format="%.4f")
    data_amt.to_excel(writer, sheet_name='LOAN_SEC_TYP', na_rep='0.00', float_format="%.4f")
    data_amt2.to_excel(writer, sheet_name='LOAN_SEC_TYP2', na_rep='0.00', float_format="%.4f")
    data_amt3.to_excel(writer, sheet_name='huankuan', na_rep='0', float_format="%.4f")
    data_amt4.to_excel(writer, sheet_name='yuqi', na_rep='0.00', float_format="%.4f")
    data_amt5.to_excel(writer, sheet_name='yuqi2', na_rep='0.00', float_format="%.4f")
    data_age.to_excel(writer, sheet_name='age', na_rep='0.00', float_format="%.4f")
    data_diyu.to_excel(writer, sheet_name='diyu', na_rep='0.00', float_format="%.4f")
    data_hk.to_excel(writer, sheet_name='hk', na_rep='0.00', float_format="%.4f")


