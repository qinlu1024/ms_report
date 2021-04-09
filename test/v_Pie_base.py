import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts import options as opts
from pyecharts.charts import Pie

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

sql_lr_fb = " SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/100000000,2) IND_VAL FROM t09_rm_indic T  " \
            "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
            "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG)  " \
            "AND T.INDIC_KEY IN (\'ZCFZ_A_113\',\'ZCFZ_B_208\') "

data_lr_fb = pd.read_sql(sql_lr_fb, engine)
data_lr_fb_p = pd.pivot_table(data_lr_fb, values='IND_VAL', index='ORG_NUM', columns='INDIC_KEY',
                              aggfunc=np.sum, fill_value=0)
data_lr_fb_p.drop(['BSBK9999'], inplace=True)
data_lr_fb_p = data_lr_fb_p.reset_index()
# print(data_lr_fb_p)
c = (
    Pie(
        init_opts=opts.InitOpts(
            width='1500px',
            height='760px',
        )
    )
    .add("",
         [list(z) for z in zip(data_lr_fb_p['ORG_NUM'], data_lr_fb_p['ZCFZ_A_113'])],
         radius=["1%", "60%"],
         center=["35%", "50%"]
         )
    .add("", [list(z) for z in zip(data_lr_fb_p['ORG_NUM'], data_lr_fb_p['ZCFZ_B_208'])],
         radius=["1%", "60%"],
         center=["75%", "50%"])
    .set_global_opts(title_opts=opts.TitleOpts(title="贷款、存款分布情况", subtitle="（单位：亿元）"),
                     legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%"))
    .render("pie_base.html")
)
