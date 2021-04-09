import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

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

sql_lr_fy = " SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic T  " \
            "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
            "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  " \
            "AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG)  " \
            "AND T.INDIC_KEY IN (\'LR_A_101\',\'LR_B_114\',\'LR_E_124\') "

data_lr_fy = pd.read_sql(sql_lr_fy, engine)
data_lr_fy_p = pd.pivot_table(data_lr_fy, values='IND_VAL', index='ORG_NUM', columns='INDIC_KEY',
                              aggfunc=np.sum, fill_value=0)
data_lr_fy_p.drop(['BSBK9999'], inplace=True)
# print(data_lr_fy_p.index.tolist())
res1 = data_lr_fy_p.reset_index()
# print(res1['ORG_NUM'].tolist())
c = (
    Bar(
        init_opts=opts.InitOpts(
            width='1600px',
            height='760px',
        )
    )
    .add_xaxis(res1['ORG_NUM'].tolist())
    .add_yaxis("营业收入", res1['LR_A_101'].tolist())
    .add_yaxis("营业支出", res1['LR_B_114'].tolist())
    .add_yaxis("净利润", res1['LR_E_124'].tolist())
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="Bar-旋转X轴标签", subtitle="解决标签名字过长的问题"),
    )
    .render("bar_rotate_xaxis_label.html")
)