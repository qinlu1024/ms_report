import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

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

sql_jg_scatter = "SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/100000000,2) IND_VAL FROM t09_rm_indic T  " \
                 "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
                 "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  AND T.ORG_LEVEL = \'3\'  " \
                 "AND T.INDIC_KEY IN (\'ZCFZ_A_113\',\'ZCFZ_B_208\') "

data_lr_fb = pd.read_sql(sql_jg_scatter, engine)
pd_lr_fb = pd.pivot_table(data_lr_fb, values='IND_VAL', columns='INDIC_KEY', index='ORG_NUM',
                          aggfunc=np.sum, fill_value=0)
res1 = pd_lr_fb.reset_index()

c = (
    Scatter()
    .add_xaxis(res1['ZCFZ_B_208'])
    .add_yaxis(
        "蒙商银行",
        [list(z) for z in zip(res1['ZCFZ_A_113'], res1['ORG_NUM'])],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                "function(params){return params.value[1] ;}"
            )
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各分行存款、贷款情况"),
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode(
                "function (params) {return params.value[2];}"
            )
        ),
        xaxis_opts=opts.AxisOpts(
            name='存款总额',
            name_location='center',
            name_gap=40,
            splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            name='贷款总额',
            name_location='center',
            name_gap=40,
            splitline_opts=opts.SplitLineOpts(is_show=True)
        )
    )
    .render("scatter_multi_dimension.html")
)
