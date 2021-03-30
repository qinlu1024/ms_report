from pyecharts import options as opts
from pyecharts.charts import Pie, Timeline
from pyecharts.faker import Faker
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
p_stat_dt = "\'2021-02-28\'"
p_curr_cd = "\'HRMB\'"
p_peroid = 'M'
p_org = "\'BSBK9999\'"

org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}
print('-------------------------------------------------------------------------------------------------------')
sql_fz_1 = "SELECT X.INDIC_KEY,X.INDIC_NAME, X.STAT_DT, ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
           "WHERE 1=1  AND X.INDIC_TYPE = \'1\' " \
           "AND X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
           "AND X.ORG_NUM = " + p_org + " " \
           "AND X.CURR_CD = " + p_curr_cd + "  " \
           "ORDER BY STAT_DT,INDIC_KEY "
# 通过pandas读取 机构数据
# data_fz_1 = pd.read_sql(sql_fz_1, engine).rename(columns={'INDIC_NAME': '指标名称'})
data_fz_1 = pd.read_sql(sql_fz_1, engine)
pd_exp_fz_1 = pd.pivot_table(data_fz_1, values='IND_VAL', index=['INDIC_KEY', 'INDIC_NAME'], columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
headers = ['科目']
for i in pd_exp_fz_1.columns.tolist():
    headers.append(i)

numsList = []
for row in pd_exp_fz_1.itertuples():
    # print(row[0][1], row[1])
    numsList.append([row[0][1], row[1], row[2], row[3], row[4]])
# print(numsList)
print('-------------------------------------------------------------------------------------------------------')
table = Table()
table.add(headers, numsList)
table.set_global_opts(
    title_opts=ComponentTitleOpts(title="资产负债表", subtitle="（单位：万元）")
)
table.render("table_base.html")
