import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

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
p_peroid = "\'M\'"
p_org = "\'BSBK9999\'"

org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}

sql_fz_2 = "SELECT X.INDIC_KEY, X.INDIC_NAME, GEN_CHAR_DATE(X.STAT_DT) STAT_DT, " \
           "ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
         "WHERE 1=1  AND X.INDIC_TYPE = \'2\' " \
         "AND X.STAT_DT <= DATE("+p_stat_dt+")  " \
         "AND X.ORG_NUM = "+p_org + " " \
         "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = \'Q\' " \
         "ORDER BY STAT_DT,INDIC_KEY "
# 抓数据
data_fz_2 = pd.read_sql(sql_fz_2, engine)
# 透视表
pd_exp_fz_2 = pd.pivot_table(data_fz_2, values='IND_VAL', index=['INDIC_KEY', 'INDIC_NAME'], columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
# 重置索引
pd_exp_fz_p2 = pd_exp_fz_2.reset_index()
# 增减值
print(pd_exp_fz_p2.columns)
tb_2 = pd_exp_fz_p2.rename(columns={'INDIC_NAME': '科目'})
rs_2 = tb_2[['科目', '2021-03-31']]
print(rs_2)

'''
headers = []
for i in rs_1.columns.tolist():
    headers.append(i)

numsList = []
for row in rs_1.round(2).itertuples():
    # print(row)
    numsList.append([row[1], row[2], row[3], row[4], row[5]])
# print(numsList)
print('-------------------------------------------------------------------------------------------------------')
table = Table()
table.add(headers, numsList)
table.set_global_opts(
    title_opts=ComponentTitleOpts(title="资产负债表", subtitle="（单位：万元）")
)
table.render("table_base2.html")
'''

