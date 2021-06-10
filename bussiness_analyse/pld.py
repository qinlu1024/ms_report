import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pyecharts.options as opts
from pyecharts.charts import Line

# 参数
p_stat_dt = "\'2021-01-31\'"
p_curr_cd = "\'HRMB\'"
p_peroid = "\'M\'"
org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}
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

# -----------------------------------    总行偏离度     ---------------------------------
sql_pld_zh = " SELECT I.INDIC_KEY,I.INDIC_NAME,I.ORG_NUM," \
             "CONCAT(YEAR(I.STAT_DT),\'年\',MONTH(I.STAT_DT),\'月\') STAT_DT ," \
             "ROUND(I.IND_VAL,4) IND_VAL " \
         " FROM t09_rm_indic I WHERE 1=1 AND I.CURR_CD = "+p_curr_cd+" AND I.INDIC_KEY = \'YS_JG_164\' " \
         " AND I.PERIOD = \'M\' AND I.STAT_DT >= " + p_stat_dt + " " \
         " AND I.ORG_NUM IN (SELECT O.ORG_NUM FROM t09_report_org O WHERE O.ORG_LEVEL = \'2\' AND O.ORG_TYPE=\'YW\') "

# 通过pandas读取 机构数据
data_pld_zh = pd.read_sql(sql_pld_zh, engine).rename(columns={'STAT_DT': '月份', 'IND_VAL': '存款偏离度', 'ORG_NUM': '机构'})
print(data_pld_zh)
'''
# style must be one of white, dark, whitegrid, darkgrid, ticks
sns.set_theme(style="ticks")
sns.lineplot(data=data_pld_zh, x='月份', y='存款偏离度', hue='机构')
plt.rcParams['font.sans-serif'] = ['STXIHEI']
plt.rcParams['axes.unicode_minus'] = False
plt.show() 

'''
data_pld_zh_1 = pd.pivot_table(data_pld_zh, values='存款偏离度', index='机构', columns='月份',
                               aggfunc=np.sum, fill_value=0)
headers = data_pld_zh_1.columns.tolist()
chart_line_data = data_pld_zh_1.reset_index()
# print(chart_line_data.info())
chart_line_data = chart_line_data.replace(org_dict)
ln = Line(
    init_opts=opts.InitOpts(
        width='1220px',
        height='760px',
    )
)
ln.add_xaxis(headers)
for row in chart_line_data.index:
    ln.add_yaxis(chart_line_data.iloc[row, 0], chart_line_data.iloc[row, 1:].to_list())
ln.set_global_opts(title_opts=opts.TitleOpts(title="蒙商银行2021年各分行月度存款偏离度情况:"),
                   legend_opts=opts.LegendOpts(orient="vertical", pos_top="10%", pos_right="2%"))
ln.render("line_base1.html")
# -----------------------------------    分行偏离度     -----------------------------------
sql_pld_fh = " SELECT I.INDIC_KEY,I.INDIC_NAME,I.ORG_NUM," \
             "CONCAT(YEAR(I.STAT_DT),\'年\',MONTH(I.STAT_DT),\'月\') STAT_DT ," \
             "ROUND(I.IND_VAL,4) IND_VAL " \
         " FROM t09_rm_indic I WHERE 1=1 AND I.CURR_CD = "+p_curr_cd+" AND I.INDIC_KEY = \'YS_JG_164\' " \
         " AND I.PERIOD = \'M\' AND I.STAT_DT >= " + p_stat_dt + " " \
         " AND I.ORG_NUM IN (SELECT O.ORG_NUM FROM t09_report_org O WHERE O.ORG_LEVEL = \'2\' AND O.ORG_TYPE=\'YW\') "
data_pld_fh = pd.read_sql(sql_pld_fh, engine)\
    .rename(columns={'STAT_DT': '月份', 'IND_VAL': '存款偏离度', 'ORG_NUM': '机构'})
data_pld_fh = data_pld_fh.replace(org_dict)

sns.set_theme(style="whitegrid")
ax = sns.stripplot(data=data_pld_fh, x='月份', y='存款偏离度', hue='机构')
plt.rcParams['font.sans-serif'] = ['STXIHEI']
plt.rcParams['axes.unicode_minus'] = False
plt.yticks([-0.2, -0.1, 0, 0.04, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
ax.axhline(y=0.04, color='red', linewidth=1, linestyle='--')
ax.axhline(y=0, color='black', linestyle='-')
plt.show()

