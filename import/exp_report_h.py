import pandas as pd
import numpy as np
from sqlalchemy import create_engine

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

# 报表基础参数
p_stat_dt = "\'2021-03-31\'"
p_curr_cd = "\'HRMB\'"
p_peroid = "\'Q\'"
org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}

# 资产负债基础数据SQL
sql_zcfz = " SELECT L.INDIC_NAME, T.INDIC_KEY,T.ORG_NUM, ROUND(T.IND_VAL/10000,2) AS IND_VAL  " \
    " FROM t00_indic_list L LEFT JOIN t09_rm_indic T ON T.INDIC_KEY = CONCAT(L.TB, \'_\', L.TYPE, \'_\', L.NBR) " \
    " AND L.IS_DISPLAY = \'1\' AND T.STAT_DT = DATE("+p_stat_dt + ") AND T.CURR_CD = "+p_curr_cd + " " \
    " AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG )  AND T.PERIOD = " + p_peroid + " " \
    " WHERE 1=1 AND L.TB = \'ZCFZ\' AND L.IS_DISPLAY = \'1\'  "\
    "ORDER BY L.DISPLAY_SEQ"

# 利润基础数据SQL
sql_lr = " SELECT L.INDIC_NAME, T.INDIC_KEY,T.ORG_NUM, ROUND(T.IND_VAL/10000,2) AS INDIC_VAL  " \
    " FROM t00_indic_list L LEFT JOIN t09_rm_indic T ON T.INDIC_KEY = CONCAT(L.TB, \'_\', L.TYPE, \'_\', L.NBR) " \
    " AND L.IS_DISPLAY = \'1\' AND T.STAT_DT = DATE("+p_stat_dt + ") AND T.CURR_CD = "+p_curr_cd + " " \
    " AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG)  AND T.PERIOD = " + p_peroid + "  " \
    " WHERE 1=1 AND L.TB = \'LR\' AND L.IS_DISPLAY = \'1\'  "\
    "ORDER BY L.DISPLAY_SEQ"
# print(sql_zcfz)
'''
# 业务状况 SQL
sql_ywzk = "SELECT Y.GL_ACCT, Y.GL_ACCT_NAME, Y.GL_ACCT_LEVEL,	Y.CURR_CD, Y.PERIOD, Y.ORG_NUM,	" \
         "Y.DR_AMT, Y.CR_AMT, Y.DR_BAL, Y.CR_BAL " \
         " FROM V_YWZK_TMP Y WHERE 1 = 1 " \
         "AND Y.ORG_NUM IN (SELECT ORG_NUM FROM V_ORG_FH) " \
         "AND Y.STAT_DT = DATE("+p_stat_dt + ") AND Y.CURR_CD = "+p_curr_cd + " "
'''
# 衍生基础数据SQL
sql_ys = " SELECT L.INDIC_NAME, L.DISPLAY_SEQ AS INDIC_KEY,L.ORG_NUM, L.IND_VAL  " \
    " FROM V_09_RM_REPORT_SHOP L " \
    " WHERE L.IS_DISPLAY = \'1\' AND L.STAT_DT = DATE("+p_stat_dt + ") AND L.CURR_CD = "+p_curr_cd + " " \
    " AND L.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG) " \
    " AND L.PERIOD = " + p_peroid + "   "

# 通过pandas读取 机构数据
data_zcfz = pd.read_sql(sql_zcfz, engine).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})
data_lr = pd.read_sql(sql_lr, engine).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})
'''
data_ywzk = pd.read_sql(sql_ywzk, engine).rename(columns={'GL_ACCT': '科目号', 'GL_ACCT_NAME': '科目名称',
                                                          'GL_ACCT_LEVEL': '科目级别', 'CURR_CD': '币种',
                                                          'PERIOD': '粒度',
                                                          'DR_AMT': '1借方发生额', 'CR_AMT': '2贷方发生额',
                                                          'DR_BAL': '3借方余额', 'CR_BAL': '3贷方余额'})
'''
data_ys = pd.read_sql(sql_ys, engine).rename(columns={'INDIC_KEY': '指标ID', 'INDIC_NAME': '指标名称'})

# print('----------------------------资产负债输出 ----------------------------------------------------------------')
pd_exp_zcfz = pd.pivot_table(data_zcfz, values='IND_VAL', index=['指标ID', '指标名称'], columns='ORG_NUM',
                             aggfunc=np.sum, fill_value=0)
pd_exp_zcfz = pd_exp_zcfz[['BSBK9999', 'BSBK9901', 'BSBK9902', 'BSBK9903', 'BSBK9904', 'BSBK9906', 'BSBK9907',
                           'BSBK9909', 'BSBK9911', 'BSBK9912', 'BSBK9913', 'BSBK9915', 'BSBK9916', 'BSBK9918',
                           'BSBK9919', 'BSBK0002', 'BSBK0001', 'BSBK0004', 'BSBKG014', 'BSBK9X03', 'BSBK9X04']]
pd_exp_zcfz = pd_exp_zcfz.rename(columns=org_dict)
# pd_exp_zcfz['均值'] = pd_exp_zcfz.mean(axis=1)
# print('----------------------------利润输出 ----------------------------------------------------------------')
pd_exp_lr = pd.pivot_table(data_lr, values='INDIC_VAL', index=['指标ID', '指标名称'], columns='ORG_NUM',
                           aggfunc=np.sum, fill_value=0)
pd_exp_lr = pd_exp_lr[['BSBK9999', 'BSBK9901', 'BSBK9902', 'BSBK9903', 'BSBK9904', 'BSBK9906', 'BSBK9907',
                       'BSBK9909', 'BSBK9911', 'BSBK9912', 'BSBK9913', 'BSBK9915', 'BSBK9916', 'BSBK9918',
                       'BSBK9919', 'BSBK0002', 'BSBK0001', 'BSBK0004', 'BSBKG014', 'BSBK9X03', 'BSBK9X04']]
pd_exp_lr = pd_exp_lr.rename(columns=org_dict)
# pd_exp_lr['均值'] = pd_exp_lr.mean(axis=1)
'''
print('----------------------------业务状况输出 ----------------------------------------------------------------')
pd_exp_ywzk = pd.pivot_table(data_ywzk, values=['1期初借方余额', '2期初贷方余额', '3借方发生额', '4贷方发生额',
                                                '5借方余额', '6贷方余额'],
                             index=['科目号', '科目名称', '科目级别', '币种', '粒度'], columns='ORG_NUM',
                             aggfunc=np.sum, fill_value=0)
 pd_exp_ywzk = pd_exp_ywzk.rename(columns=org_dict)
 pd_exp_ywzk.to_excel('D:\\test\\业务状况表' + p_stat_dt + '.xls', sheet_name='业务状况表', na_rep=0, float_format="%.2f")
 '''

# print('----------------------------衍生指标输出 ----------------------------------------------------------------')
pd_exp_ys = pd.pivot_table(data_ys, values='IND_VAL', index=['指标ID', '指标名称'], columns='ORG_NUM',
                           aggfunc=np.sum, fill_value=0)
pd_exp_ys = pd_exp_ys[['BSBK9999', 'BSBK9901', 'BSBK9902', 'BSBK9903', 'BSBK9904', 'BSBK9906', 'BSBK9907',
                       'BSBK9909', 'BSBK9911', 'BSBK9912', 'BSBK9913', 'BSBK9915', 'BSBK9916', 'BSBK9918',
                       'BSBK9919', 'BSBK0002', 'BSBK0001', 'BSBK0004', 'BSBKG014', 'BSBK9X03', 'BSBK9X04']]
pd_exp_ys = pd_exp_ys.rename(columns=org_dict)
# pd_exp_ys['均值'] = pd_exp_ys.mean(axis=1)
# pd_exp_ys.to_excel('D:\\test\\衍生表' + p_stat_dt + '.xls', sheet_name='利润表', na_rep=0, float_format="%.2f")

# print('---------------------------- excel输出 ----------------------------------------------------------------')
with pd.ExcelWriter('D:\\test\\各分行jj度横向_('+p_stat_dt[1:11]+').xlsx') as writer:
    pd_exp_ys.to_excel(writer, sheet_name='衍生指标', na_rep=0, float_format="%.4f")
    pd_exp_zcfz.to_excel(writer, sheet_name='资产负债', na_rep=0, float_format="%.2f")
    pd_exp_lr.to_excel(writer, sheet_name='利润表', na_rep=0, float_format="%.2f")
#    pd_exp_ywzk.to_excel(writer, sheet_name='业务状况表', na_rep=0, float_format="%.2f")
