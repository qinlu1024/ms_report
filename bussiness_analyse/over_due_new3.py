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
win_test = 'rcjc'
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
sql_dis = " SELECT L.ACTV_MON,L.BHDT_BCH_CDE,L.PRODUCT_TYP,L.LOAN_TYP,L.DIS_AMT, L.ACT_NBR " \
          " FROM dis_amt L WHERE 1=1 " \
          " AND L.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') "
data_dis = pd.read_sql(sql_dis, engine)
data_dis['LOAN_TYP'].replace(loan_typ_dict, inplace=True)
data_dis['BHDT_BCH_CDE'] = 'BSBK99' + data_dis['BHDT_BCH_CDE']
data_dis.replace(org_dict, inplace=True)
data_dis.rename(columns=col_dict, inplace=True)


sql_res = " SELECT P.ACTV_MON,P.TRD_MON,P.MON_DIF,P.BHDT_BCH_CDE,P.PRODUCT_TYP,P.LOAN_TYP,P.RES_AMT " \
          " FROM BASE_AMT P WHERE 1=1 " \
          " AND P.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') "
data_res = pd.read_sql(sql_res, engine)
data_res['LOAN_TYP'].replace(loan_typ_dict, inplace=True)
data_res['RES_AMT'] = data_res['RES_AMT'].fillna(0)
data_res['BHDT_BCH_CDE'] = 'BSBK99' + data_res['BHDT_BCH_CDE']
data_res.rename(columns=col_dict, inplace=True)
data_res_p1 = pd.pivot_table(data_res, values='本金余额', columns='MON_DIF',
                             index=['放款月份', '放款分行', '产品类型', '贷款类型'], fill_value=0)
data_res_p1.rename(index=org_dict, inplace=True)


sql_due = " SELECT P.ACTV_MON,P.TRD_MON,P.MON_DIF,P.BHDT_BCH_CDE,P.PRODUCT_TYP,P.LOAN_TYP,P.RES_AMT " \
          " FROM DUE_AMT P WHERE 1=1 " \
          " AND P.BHDT_BCH_CDE NOT IN (\'05\',\'08\',\'10\',\'14\') "
data_due = pd.read_sql(sql_due, engine)
data_due['LOAN_TYP'].replace(loan_typ_dict, inplace=True)
data_due['RES_AMT'] = data_due['RES_AMT'].fillna(0)
data_due['BHDT_BCH_CDE'] = 'BSBK99' + data_due['BHDT_BCH_CDE']
data_due.rename(columns=col_dict, inplace=True)
data_due_p1 = pd.pivot_table(data_due, values='本金余额', columns='MON_DIF',
                             index=['放款月份', '放款分行', '产品类型', '贷款类型'], fill_value=0)
data_due_p1.rename(index=org_dict, inplace=True)

data_due_p3 = data_due_p1.div(data_res_p1)

# 生成数据报表
with pd.ExcelWriter('D:\\test\\due_list24.xlsx') as writer:
    data_dis.to_excel(writer, sheet_name='放款总额', na_rep='0', float_format="%.4f")
    data_res_p1.to_excel(writer, sheet_name='还款计划本金余额', na_rep='0', float_format="%.4f")
    data_due_p1.to_excel(writer, sheet_name='逾期总额', na_rep='0', float_format="%.4f")
    data_due_p3.to_excel(writer, sheet_name='逾期分析', na_rep='0', float_format="%.4f")