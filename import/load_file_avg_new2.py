import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# 参数
# 报表路径、Sheet页名称
p_report_path = 'D:\\Data_File\\new2.0\\20210630_M_AVG.xls'
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
avg_df = pd.read_excel(p_report_path,
                       sheet_name=p_report_sheet_name,
                       dtype={'GL_ACCT': str,
                              'F_CURR_CD': str,
                              'OP_ORG_NUM': str,
                              'CURR_CD': str,
                              'GL_BAL_TYPE_CD': str,
                              'NBR': int
                              }
                       )
avg_df['PERIOD'] = p_period

# 日期\金额 转换
avg_df['STAT_DT'] = pd.to_datetime(avg_df['STAT_DT'], format='%Y%m%d')
avg_df['LAST_D_BAL'] = pd.to_numeric(avg_df['LAST_D_BAL'], errors='coerce').fillna(0)
avg_df['LAST_C_BAL'] = pd.to_numeric(avg_df['LAST_C_BAL'], errors='coerce').fillna(0)

avg_df['DR_AMT'] = pd.to_numeric(avg_df['DR_AMT'], errors='coerce').fillna(0)
avg_df['MIN_DR_AMT'] = pd.to_numeric(avg_df['MIN_DR_AMT'], errors='coerce').fillna(0)
avg_df['MAX_DR_AMT'] = pd.to_numeric(avg_df['MAX_DR_AMT'], errors='coerce').fillna(0)
avg_df['STD_DR_AMT'] = pd.to_numeric(avg_df['STD_DR_AMT'], errors='coerce').fillna(0)

avg_df['CR_AMT'] = pd.to_numeric(avg_df['CR_AMT'], errors='coerce').fillna(0)
avg_df['MIN_CR_AMT'] = pd.to_numeric(avg_df['MIN_CR_AMT'], errors='coerce').fillna(0)
avg_df['MAX_CR_AMT'] = pd.to_numeric(avg_df['MAX_CR_AMT'], errors='coerce').fillna(0)
avg_df['STD_CR_AMT'] = pd.to_numeric(avg_df['STD_CR_AMT'], errors='coerce').fillna(0)

avg_df['DR_BAL'] = pd.to_numeric(avg_df['DR_BAL'], errors='coerce').fillna(0)
avg_df['MIN_DR_BAL'] = pd.to_numeric(avg_df['MIN_DR_BAL'], errors='coerce').fillna(0)
avg_df['MAX_DR_BAL'] = pd.to_numeric(avg_df['MAX_DR_BAL'], errors='coerce').fillna(0)
avg_df['STD_DR_BAL'] = pd.to_numeric(avg_df['STD_DR_BAL'], errors='coerce').fillna(0)

avg_df['CR_BAL'] = pd.to_numeric(avg_df['CR_BAL'], errors='coerce').fillna(0)
avg_df['MIN_CR_BAL'] = pd.to_numeric(avg_df['MIN_CR_BAL'], errors='coerce').fillna(0)
avg_df['MAX_CR_BAL'] = pd.to_numeric(avg_df['MAX_CR_BAL'], errors='coerce').fillna(0)
avg_df['STD_CR_BAL'] = pd.to_numeric(avg_df['STD_CR_BAL'], errors='coerce').fillna(0)

des_df = avg_df.loc[:, ['STAT_DT', 'OP_ORG_NUM', 'CURR_CD', 'GL_ACCT', 'PERIOD', 'GL_BAL_TYPE_CD',
                        'LAST_D_BAL', 'LAST_C_BAL',
                        'DR_AMT', 'MIN_DR_AMT', 'MAX_DR_AMT', 'STD_DR_AMT',
                        'CR_AMT', 'MIN_CR_AMT', 'MAX_CR_AMT', 'STD_CR_AMT',
                        'DR_BAL', 'MIN_DR_BAL', 'MAX_DR_BAL', 'STD_DR_BAL',
                        'CR_BAL', 'MIN_CR_BAL', 'MAX_CR_BAL', 'STD_CR_BAL',
                        'NBR']]
des_df.to_sql('t09_gl_subj_avg_month', engine,
              if_exists='append', index=False,
              dtype={
                  "stat_dt": sqlalchemy.types.DATE,
                  "op_org_num": sqlalchemy.types.String(length=20),
                  "curr_cd": sqlalchemy.types.String(length=8),
                  "gl_acct": sqlalchemy.types.String(length=20),
                  "gl_bal_type_cd": sqlalchemy.types.String(length=2)
              })
print('*'*15 + '  complete data import !!  ' + '*'*15)
