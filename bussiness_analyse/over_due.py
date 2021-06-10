from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# 数据库用户名
win_user = 'root'
# 数据库密码
win_password = '123456'
# 数据库ip地址
win_host = '127.0.0.1'
# 端口号
win_port = 3306
# 数据库
win_test = 'rcjc'
engine = create_engine(f'mysql+pymysql://{win_user}:{win_password}@{win_host}:{win_port}/{win_test}', echo=True)

sql_dis = " SELECT L.ACTV_MON,L.BHDT_BCH_CDE,L.PRODUCT_TYP,L.LOAN_TYP,L.DIS_AMT, L.ACT_NBR FROM dis_amt L "
# 通过pandas读取 机构数据
data_dis = pd.read_sql(sql_dis, engine)
# print(data_dis.head())

sql_res = " SELECT P.ACTV_MON,P.INT_DUE_MON, P.BHDT_BCH_CDE, P.PRODUCT_TYP, P.LOAN_TYP, P.RES_AMT FROM PLAN_AMT P "
data_res = pd.read_sql(sql_res, engine)
data_res['RES_AMT'] = data_res['RES_AMT'].fillna(0)
data_res_p1 = pd.pivot_table(data_res, values='RES_AMT', columns='INT_DUE_MON',
                             index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)
# data_res_p2 = data_res_p1.reset_index()

sql_due = " SELECT D.ACTV_MON, D.ETL_DATE2 AS INT_DUE_MON, D.BHDT_BCH_CDE, D.PRODUCT_TYP, D.LOAN_TYP , D.RES_AMT " \
          " FROM due_amt D "
data_due = pd.read_sql(sql_due, engine)
# print(data_due.head())
data_due['RES_AMT'] = data_due['RES_AMT'].fillna(0)
data_due_p1 = pd.pivot_table(data_due, values='RES_AMT', columns='INT_DUE_MON',
                             index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)
# data_due_p2 = data_due_p1.reset_index()
data_due_p3 = data_due_p1.div(data_res_p1)

sql_yql = " SELECT L.ACTV_MON,L.BHDT_BCH_CDE,L.PRODUCT_TYP,L.LOAN_TYP, D.ETL_DATE2 , (D.RES_AMT/L.DIS_AMT) YQ " \
          " FROM dis_amt L , due_amt D WHERE 1=1 " \
          " AND L.ACTV_MON = D.ACTV_MON " \
          " AND L.BHDT_BCH_CDE = D.BHDT_BCH_CDE " \
          " AND L.PRODUCT_TYP = D.PRODUCT_TYP " \
          " AND L.LOAN_TYP = D.LOAN_TYP "
data_yql = pd.read_sql(sql_yql, engine)
data_yql_p1 = pd.pivot_table(data_yql, values='YQ', columns='ETL_DATE2',
                             index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)

with pd.ExcelWriter('D:\\test\\due_list10.xlsx') as writer:
    data_dis.to_excel(writer, sheet_name='dis_list', na_rep='0', float_format="%.4f")
    data_res_p1.to_excel(writer, sheet_name='res_list', na_rep='0', float_format="%.4f")
    data_due_p1.to_excel(writer, sheet_name='due_list', na_rep='0', float_format="%.4f")
    data_due_p3.to_excel(writer, sheet_name='add', na_rep='0', float_format="%.4f")
    data_yql_p1.to_excel(writer, sheet_name='yql', na_rep='0', float_format="%.4f")
