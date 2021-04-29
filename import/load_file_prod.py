import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# 参数
# 报表路径、Sheet页名称
p_report_path = 'D:\\Data_File\\model_5020_929315.xls'
p_report_sheet_name = 'FDM_F_PROD_ACC_BAL'
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
prod_df = pd.read_excel(p_report_path, sheet_name=p_report_sheet_name, dtype={'SN': str, 'OP_CD': str,
                                                                              'BAL_CD_FLG': str,
                                                                              'PROD_CD': str, 'CURR_CD': str,
                                                                              'CALC_UNIT_ID': str, 'INST_CD': str,
                                                                              'LOAD_DT': str,
                                                                              'GL_ACC_ID': str, 'EFF_FLG': str})
# 日期\金额 转换
prod_df['PREV_DR_BAL_AMT'] = pd.to_numeric(prod_df['PREV_DR_BAL_AMT'], errors='coerce')
prod_df['PREV_CR_BAL_AMT'] = pd.to_numeric(prod_df['PREV_CR_BAL_AMT'], errors='coerce')
prod_df['CUR_DR_AMT'] = pd.to_numeric(prod_df['CUR_DR_AMT'], errors='coerce')
prod_df['CUR_CR_AMT'] = pd.to_numeric(prod_df['CUR_CR_AMT'], errors='coerce')
prod_df['CUR_DR_BAL_AMT'] = pd.to_numeric(prod_df['CUR_DR_BAL_AMT'], errors='coerce')
prod_df['CUR_CR_BAL_AMT'] = pd.to_numeric(prod_df['CUR_CR_BAL_AMT'], errors='coerce')

# number null 值处理
prod_df['PREV_DR_BAL_AMT'] = prod_df['PREV_DR_BAL_AMT'].fillna(0)
prod_df['PREV_CR_BAL_AMT'] = prod_df['PREV_CR_BAL_AMT'].fillna(0)
prod_df['CUR_DR_AMT'] = prod_df['CUR_DR_AMT'].fillna(0)
prod_df['CUR_CR_AMT'] = prod_df['CUR_CR_AMT'].fillna(0)
prod_df['CUR_DR_BAL_AMT'] = prod_df['CUR_DR_BAL_AMT'].fillna(0)
prod_df['CUR_CR_BAL_AMT'] = prod_df['CUR_CR_BAL_AMT'].fillna(0)
# order by
des_df = prod_df.loc[:, ['SN', 'PROD_CD', 'CALC_UNIT_ID', 'GL_ACC_ID', 'OP_CD', 'BAL_CD_FLG', 'CURR_CD',
                         'INST_CD', 'PREV_DR_BAL_AMT', 'PREV_CR_BAL_AMT', 'CUR_DR_AMT', 'CUR_CR_AMT',
                         'CUR_DR_BAL_AMT', 'CUR_CR_BAL_AMT',
                         'LOAD_DT', 'EFF_BGN_DT', 'EFF_END_DT', 'EFF_FLG']]
# load data
des_df.to_sql('t00_fdm_f_prod_acc_bal', engine, if_exists='append', index=False)
print('*'*30 + '  Complete data import !!   ' + '*'*30)
