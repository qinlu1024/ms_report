import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# 参数
# 报表路径、Sheet页名称
p_report_path = 'D:\\Data_File\\20201130_ST.xls'
p_report_sheet_name = 'gl_subj_month'
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
                                                                             'GL_BAL_TYPE_CD': str})
avg_df['PERIOD'] = p_period
print('----------------------------- 1. report 格式处理 ---------------------------------------------------------------')
# 日期\金额 转换
avg_df['STAT_DT'] = pd.to_datetime(avg_df['STAT_DT'], format='%Y%m%d')
avg_df['LAST_D_BAL'] = pd.to_numeric(avg_df['LAST_D_BAL'], errors='coerce')
avg_df['LAST_C_BAL'] = pd.to_numeric(avg_df['LAST_C_BAL'], errors='coerce')
avg_df['DR_AMT'] = pd.to_numeric(avg_df['DR_AMT'], errors='coerce')
avg_df['CR_AMT'] = pd.to_numeric(avg_df['CR_AMT'], errors='coerce')
avg_df['DR_BAL'] = pd.to_numeric(avg_df['DR_BAL'], errors='coerce')
avg_df['CR_BAL'] = pd.to_numeric(avg_df['CR_BAL'], errors='coerce')
print('----------------------------number null 值处理 ----------------------------------------------------------------')
avg_df['LAST_D_BAL'] = avg_df['LAST_D_BAL'].fillna(0)
avg_df['LAST_C_BAL'] = avg_df['LAST_C_BAL'].fillna(0)
avg_df['DR_AMT'] = avg_df['DR_AMT'].fillna(0)
avg_df['CR_AMT'] = avg_df['CR_AMT'].fillna(0)
avg_df['DR_BAL'] = avg_df['DR_BAL'].fillna(0)
avg_df['CR_BAL'] = avg_df['CR_BAL'].fillna(0)
print('-----------------------------report 格式处理 完成 ---------------------------------------------------------------')
# report 格式处理 完成
des_df = avg_df.loc[:, ['STAT_DT', 'OP_ORG_NUM', 'CURR_CD', 'GL_ACCT', 'PERIOD', 'GL_BAL_TYPE_CD',
                        'LAST_D_BAL', 'LAST_C_BAL',
                        'DR_AMT', 'CR_AMT',
                        'DR_BAL', 'CR_BAL']]

des_df.to_sql('t09_gl_subj_month', engine,
              if_exists='append', index=False,
              dtype={
                  "STAT_DT": sqlalchemy.types.DATE,
                  "OP_ORG_NUM": sqlalchemy.types.String(length=20),
                  "CURR_CD": sqlalchemy.types.String(length=8),
                  "GL_ACCT": sqlalchemy.types.String(length=20),
                  "GL_BAL_TYPE_CD": sqlalchemy.types.String(length=2)
              })

print('*'*30 + '  Complete data import !!   ' + '*'*30)
