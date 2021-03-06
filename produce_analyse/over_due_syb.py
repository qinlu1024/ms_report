import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns

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

org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}
col_dict = {'ACTV_MON': '放款月份', 'BHDT_BCH_CDE': '放款分行', 'PRODUCT_TYP': '产品类型', 'LOAN_TYP': '贷款类型',
            'DIS_AMT': '放款金额', 'ACT_NBR': '放款笔数', 'INT_DUE_MON': '观察月份', 'RES_AMT': '本金余额',
            'ETL_DATE2': '观察月份', 'YQ': '逾期率', 'TRD_MON': '观察月份'}
loan_typ_dict = {'零押贷(授信)': '零押贷', '零押贷个人信用消费贷款': '零押贷', '马上贷消费贷款': '马上贷', '保商赢(存量)': '保商赢'}

# ------------------------------------------- 分割线 -------------------------------------------------------------------
# 放款
sql_dis = " SELECT L.ACTV_MON,L.BHDT_BCH_CDE,L.PRODUCT_TYP,L.LOAN_TYP,L.DIS_AMT, L.NBR " \
          " FROM LOAN_DIS_AMT L WHERE 1=1 " \
          " AND L.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') " \
          " AND L.LOAN_TYP = \'丰收贷\' "
data_dis = pd.read_sql(sql_dis, engine)
# data_dis['LOAN_TYP'].replace(loan_typ_dict, inplace=True)
# data_dis['BHDT_BCH_CDE'] = 'BSBK99' + data_dis['BHDT_BCH_CDE']
# data_dis.replace(org_dict, inplace=True)　
# data_dis.rename(columns=col_dict, inplace=True)

# 逾期
sql_due = " SELECT P.ACTV_MON,P.TRD_MON,P.MON_DIF,P.BHDT_BCH_CDE,P.PRODUCT_TYP,P.LOAN_TYP, P.NBR, P.RES_AMT " \
          " FROM LOAN_DUE_AMT P WHERE 1=1 " \
          " AND P.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') " \
          " AND P.LOAN_TYP = \'丰收贷\' "
data_due = pd.read_sql(sql_due, engine)
# data_due['LOAN_TYP'].replace(loan_typ_dict, inplace=True)
# data_due['RES_AMT'] = data_due['RES_AMT'].fillna(0)
# data_due['BHDT_BCH_CDE'] = 'BSBK99' + data_due['BHDT_BCH_CDE']
# data_due.rename(columns=col_dict, inplace=True)
data_due_p1 = pd.pivot_table(data_due, values='RES_AMT', columns='TRD_MON',
                             index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)
# data_due_p1.rename(index=org_dict, inplace=True)


sql_yql = " SELECT L.ACTV_MON, P.TRD_MON, P.MON_DIF, L.BHDT_BCH_CDE, L.PRODUCT_TYP, L.LOAN_TYP, " \
          " P.NBR/L.NBR NBR_P ,P.NBR NBRP, L.NBR NBRL, P.RES_AMT/L.DIS_AMT AMT_P  " \
          " FROM  LOAN_DIS_AMT L , loan_due_amt P  " \
          " WHERE 1 = 1   AND L.ACTV_MON = P.ACTV_MON   AND L.BHDT_BCH_CDE = P.BHDT_BCH_CDE " \
          " AND L.PRODUCT_TYP = P.PRODUCT_TYP   AND L.LOAN_TYP = P.LOAN_TYP " \
          " AND P.MON_DIF > 0 " \
          " AND L.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') " \
          " AND L.LOAN_TYP = \'丰收贷\' "
data_yql = pd.read_sql(sql_yql, engine)
data_yql_amt = pd.pivot_table(data_yql, values='AMT_P', columns='TRD_MON',
                              index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)
data_yql_nbr = pd.pivot_table(data_yql, values='NBR_P', columns='TRD_MON',
                              index=['ACTV_MON', 'BHDT_BCH_CDE', 'PRODUCT_TYP', 'LOAN_TYP'], fill_value=0)


# 生成数据报表
with pd.ExcelWriter('D:\\test\\due_list44.xlsx') as writer:
    data_dis.to_excel(writer, sheet_name='放款总额', na_rep='0.00', float_format="%.4f")
    # data_res_p1.to_excel(writer, sheet_name='还款计划本金余额', na_rep='0', float_format="%.4f")
    data_due_p1.to_excel(writer, sheet_name='逾期总额', na_rep='0.00', float_format="%.4f")
    data_yql_amt.to_excel(writer, sheet_name='逾期分析', na_rep='0.00', float_format="%.4f")
    data_yql_nbr.to_excel(writer, sheet_name='逾期笔数分析', na_rep='0.00', float_format="%.2f")
    data_yql.to_excel(writer, sheet_name='逾期分析笔数2', na_rep='0', float_format="%.4f")

