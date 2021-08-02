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
org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}
'''
sql_v01 = " SELECT * FROM T_loan_s01_fsd "

# 通过pandas读取 机构数据
data_v01 = pd.read_sql(sql_v01, engine)
data_v01['INT_START_DT'] = pd.to_datetime(data_v01['INT_START_DT'], format="%Y/%m/%d")
data_v01['LAST_DUE_DT'] = pd.to_datetime(data_v01['LAST_DUE_DT'], format="%Y/%m/%d")
data_v01['ACTV_DT'] = pd.to_datetime(data_v01['ACTV_DT'], format="%Y/%m/%d")
data_v01['LAST_SETL_DT'] = pd.to_datetime(data_v01['LAST_SETL_DT'], format="%Y/%m/%d")


sns.set_theme(style="darkgrid")
sns.displot(data_v01['AGE'], binwidth=3)
# sns.displot(data_v01['FKQX'], kde=True)
# sns.displot(data_v01['DIS_AMT'], kde=True)
plt.show()

hz_describe = data_v01.describe()
data_fh_gp = data_v01.groupby('FH')
des_all = data_fh_gp.describe()
fh_dis_amt = data_fh_gp['DIS_AMT'].sum()
# data_v01.replace(col_dict, inplace=True)
# print(data_fh.describe())
# print(fh_dis_amt)
data_amt = pd.pivot_table(data_v01, values=['DIS_AMT', 'BASE_AMT', 'PINT_AMT'], index='FH', columns='SETL_FLG',
                          aggfunc=np.sum, margins=True)
data_due = pd.pivot_table(data_v01, values='BASE_AMT', index='FH', columns='LOAN_CLASS',
                          aggfunc=np.sum, margins=True)
data_rep = pd.pivot_table(data_v01, values='BASE_AMT', index='REP_CATE', columns='LOAN_CLASS',
                          aggfunc=np.sum, margins=True)


bins = [0, 20, 30, 40, 50, 60, 100]
sql_age = " SELECT * FROM V_LOAN_FSD_AGE "
data_age = pd.read_sql(sql_age, engine)
group_name = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-100']

data_age['AGE_RANK'] = pd.cut(data_age['AGE'], bins, labels=group_name)
# data_age_gb = data_age.groupby('AGE_RANK')
data_age_piv = pd.pivot_table(data_age,  values=['NBR', 'P_NBR', 'DIS_AMT', 'BASE_AMT', 'DUE_BASE', 'FYJ_BASE'],
                              index='AGE_RANK', aggfunc=np.sum)


with pd.ExcelWriter('D:\\test\\fsd-06.xlsx') as writer:
    hz_describe.to_excel(writer, sheet_name='zh_describe', na_rep='0.00', float_format="%.4f")
    des_all.to_excel(writer, sheet_name='describe', na_rep='0.00', float_format="%.4f")
    data_amt.to_excel(writer, sheet_name='SETL_FLG', na_rep='0.00', float_format="%.4f")
    data_due.to_excel(writer, sheet_name='LOAN_CLASS', na_rep='0.00', float_format="%.4f")
    data_rep.to_excel(writer, sheet_name='REP_CATE', na_rep='0.00', float_format="%.4f")
    data_age_piv.to_excel(writer, sheet_name='AGE', na_rep='0.00', float_format="%.4f")

sql_v02 = " SELECT * FROM T_loan_s01_fsd3 T WHERE 1=1 AND T.SETL_FLG = \'Y\' "


# 通过pandas读取 机构数据
data_v02 = pd.read_sql(sql_v02, engine)
data_v02['INT_START_DT'] = pd.to_datetime(data_v02['INT_START_DT'], format="%Y/%m/%d")
data_v02['LAST_DUE_DT'] = pd.to_datetime(data_v02['LAST_DUE_DT'], format="%Y/%m/%d")
data_v02['ACTV_DT'] = pd.to_datetime(data_v02['ACTV_DT'], format="%Y/%m/%d")
data_v02['LAST_SETL_DT'] = pd.to_datetime(data_v02['LAST_SETL_DT'], format="%Y/%m/%d")

data_v02['TQ_DAY'] = data_v02['FKQX'] - data_v02['YKQX']
print("------------data_v02------------")
sns.set_theme(style="darkgrid")
sns.displot(data_v02['TQ_DAY'], binwidth=3)
# sns.displot(data_v01['FKQX'], kde=True)
# sns.displot(data_v01['DIS_AMT'], kde=True)
plt.show()

sql_v03 = " SELECT X.LOAN_NO,X.ACTV_DT,X.DIS_AMT, date(X.OPEN_DT) OPEN_DT,X.LOAN_CLASS, " \
          " (X.BASE_AMT-X.BASE_AMT_P) BASE_AMT ,X.EXCU_RATE, X.PINT_AMT, " \
          " DATEDIFF(X.ACTV_DT , date(X.OPEN_DT)) OPEN_DAYS " \
          " FROM t_loan_s01_fsd3 X  WHERE 1=1 AND X.OPEN_DT > '20000101' AND X.ACTV_DT < DATE(\'2020-07-01\') " \
          " AND X.EXCU_RATE IS NOT NULL "
data_v03 = pd.read_sql(sql_v03, engine)
data_v03['ACTV_DT'] = pd.to_datetime(data_v03['ACTV_DT'], format="%Y/%m/%d")
data_v03['OPEN_DT'] = pd.to_datetime(data_v03['OPEN_DT'], format="%Y/%m/%d")
# data_v03['OPEN_YEAR'] = data_v03['OPEN_DAYS']/365
data_v03['OPEN_YEAR'] = data_v03['OPEN_DAYS']
# data_v03['OPEN_YEAR'] = data_v03['OPEN_YEAR'].astype('int')
print(data_v03.head())
'''

sql_v04 = " SELECT DATEDIFF(DATE(D.ACTV_DT),date(TRIM(D.LAST_DUE_DT_MAX))) DATE_DIFF FROM LOAN_XD D " \
          " WHERE D.LOAN_NBR > 0 "
data_v04 = pd.read_sql(sql_v04, engine)
print(data_v04.describe())
bins = [0, 10, 30, 40, 50, 60, 100]

sns.set_theme(style="darkgrid")
# sns.displot(data_v03['OPEN_YEAR'], binwidth=3)
sns.displot(data_v04['DATE_DIFF'])
# sns.displot(data_v01['FKQX'], kde=True)
# sns.displot(data_v01['DIS_AMT'], kde=True)
plt.show()


