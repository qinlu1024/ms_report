import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# 参数
# 报表路径、Sheet页名称
p_report_path = 'D:\\Data_File\\new\\2021-03-31-AVG.xls'
p_report_sheet_name = 'gl_subj_month_avg'
p_period = 'M'
# p_curr_cd = 'HRMB'
# 数据库用户名
win_user = 'root'
# 数据库密码
win_password = '123456'
# 数据库ip地址
win_host = '127.0.0.1'
# 端口号
win_port = 3306
# 数据库
win_test = 'regular_monitoring'
engine = create_engine(f'mysql+pymysql://{win_user}:{win_password}@{win_host}:{win_port}/{win_test}', echo=True)
# ---------------------------------------! GO GO GO !------------------------------------------------------------------
# report to DF
avg_df = pd.read_excel(p_report_path, sheet_name=p_report_sheet_name, dtype={'GL_ACCT': str,
                                                                             'F_CURR_CD': str,
                                                                             'OP_ORG_NUM': str,
                                                                             'CURR_CD': str,
                                                                             'GL_BAL_TYPE_CD': str,
                                                                             'NBR': int})
avg_df['period'] = p_period
print('----------------------------- 1. report 格式处理 ---------------------------------------------------------------')
# 日期\金额 转换
avg_df['stat_dt'] = pd.to_datetime(avg_df['stat_dt'], format='%Y-%m-%d')
avg_df['last_d_bal'] = pd.to_numeric(avg_df['last_d_bal'], errors='coerce')
avg_df['last_c_bal'] = pd.to_numeric(avg_df['last_c_bal'], errors='coerce')

avg_df['dr_amt'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')
avg_df['min_dr_amt'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')
avg_df['max_dr_amt'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')

avg_df['cr_amt'] = pd.to_numeric(avg_df['cr_amt'], errors='coerce')
avg_df['min_cr_amt'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')
avg_df['max_cr_amt'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')

avg_df['dr_bal'] = pd.to_numeric(avg_df['dr_bal'], errors='coerce')
avg_df['min_dr_bal'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')
avg_df['max_dr_bal'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')

avg_df['cr_bal'] = pd.to_numeric(avg_df['cr_bal'], errors='coerce')
avg_df['min_cr_bal'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')
avg_df['max_cr_bal'] = pd.to_numeric(avg_df['dr_amt'], errors='coerce')

print('----------------------------number null ?????? ----------------------------------------------------------------')
avg_df['last_d_bal'] = avg_df['last_d_bal'].fillna(0)
avg_df['last_c_bal'] = avg_df['last_c_bal'].fillna(0)
avg_df['dr_amt'] = avg_df['dr_amt'].fillna(0)
avg_df['cr_amt'] = avg_df['cr_amt'].fillna(0)
avg_df['dr_bal'] = avg_df['dr_bal'].fillna(0)
avg_df['cr_bal'] = avg_df['cr_bal'].fillna(0)
avg_df['min_dr_amt'] = avg_df['min_dr_amt'].fillna(0)
avg_df['max_dr_amt'] = avg_df['max_dr_amt'].fillna(0)
avg_df['min_cr_amt'] = avg_df['min_cr_amt'].fillna(0)
avg_df['max_cr_amt'] = avg_df['max_cr_amt'].fillna(0)
avg_df['min_dr_bal'] = avg_df['min_dr_bal'].fillna(0)
avg_df['max_dr_bal'] = avg_df['max_dr_bal'].fillna(0)
avg_df['min_cr_bal'] = avg_df['min_cr_bal'].fillna(0)
avg_df['max_cr_bal'] = avg_df['max_cr_bal'].fillna(0)
print('-----------------------------report 格式处理 完成 ---------------------------------------------------------------')
# report 格式处理 完成

des_df = avg_df.loc[:, ['stat_dt', 'op_org_num', 'curr_cd', 'gl_acct', 'period', 'gl_bal_type_cd',
                        'last_d_bal', 'last_c_bal',
                        'dr_amt', 'min_dr_amt', 'max_dr_amt',
                        'cr_amt', 'min_cr_amt', 'max_cr_amt',
                        'dr_bal', 'min_dr_bal', 'max_dr_bal',
                        'cr_bal', 'min_cr_bal', 'max_cr_bal',
                        'nbr']]
des_df.to_sql('t09_gl_subj_avg_month_new', engine,
              if_exists='append', index=False,
              dtype={
                  "stat_dt": sqlalchemy.types.DATE,
                  "op_org_num": sqlalchemy.types.String(length=20),
                  "curr_cd": sqlalchemy.types.String(length=8),
                  "gl_acct": sqlalchemy.types.String(length=20),
                  "gl_bal_type_cd": sqlalchemy.types.String(length=2)
              })
print('*'*15 + '  complete data import !!   ' + '*'*15)
