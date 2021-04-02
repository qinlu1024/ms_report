from pyecharts import options as opts
from pyecharts.charts import Pie, Timeline
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
p_stat_dt = "\'2021-02-28\'"
p_curr_cd = "\'HRMB\'"
p_peroid = 'M'
p_org = "\'BSBK9999\'"

sql_indic_map = "SELECT CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR) AS INDIC_KEY,L.INDIC_NAME FROM t00_indic_list L " \
                "WHERE 1=1  AND TB=\'ZCFZ\'  AND IS_DISPLAY = \'1\'  ORDER BY DISPLAY_SEQ    " \

sql_fz_1 =  " SELECT T.INDIC_KEY, T.STAT_DT, ROUND(T.IND_VAL/10000,2) IND_VAL FROM T09_RM_INDIC T,T00_INDIC_LIST L " \
             "WHERE 1=1 AND T.INDIC_KEY = CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR)  AND L.TB = \'ZCFZ\'  " \
             "AND T.CURR_CD =\'HRMB\'  AND L.TB = \'ZCFZ\'  AND L.TYPE = \'A\'  AND L.NBR < \'127\' " \
             "AND T.STAT_DT <= DATE(" + p_stat_dt + ")  " \
             "AND T.ORG_NUM = " + p_org + " " \
             "AND T.CURR_CD = " + p_curr_cd + "  " \
             "ORDER BY STAT_DT,INDIC_KEY "

# 通过pandas读取 机构数据
data_map = pd.read_sql(sql_indic_map, engine, index_col='INDIC_KEY')
data_dict = data_map.to_dict()['INDIC_NAME']
data_fz_1 = pd.read_sql(sql_fz_1, engine)

pd_exp_fz_1 = pd.pivot_table(data_fz_1, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
headers = pd_exp_fz_1.columns.tolist()
pd_exp_fz_2 = pd_exp_fz_1.reset_index()
pd_exp_fz_2 = pd_exp_fz_2.replace(data_dict)

tl = Timeline(
    # 初始化配置项
    init_opts=opts.InitOpts(

        width='1220px',
        height='900px',
    )
)
for it in headers:
    tmp = pd_exp_fz_2[['INDIC_KEY', it]]
    pie = (
        Pie(

        )
        .add(
            "资产负债表",
            [list(z) for z in zip(tmp['INDIC_KEY'], tmp[it])],

            # 是否展示成南丁格尔图，通过半径区分数据大小，有'radius'和'area'两种模式。
            # radius：扇区圆心角展现数据的百分比，半径展现数据的大小
            # area：所有扇区圆心角相同，仅通过半径展现数据大小
            rosetype="radius",
            # 饼图的半径，数组的第一项是内半径，第二项是外半径
            # 默认设置成百分比，相对于容器高宽中较小的一项的一半
            radius=["30%", "60%"],

            label_opts=opts.LabelOpts(position="center")

            # 提示框组件配置项，参考 `series_options.TooltipOpts`
            # tooltip_opts= Union[opts.TooltipOpts, dict, None] = None,
        )
        .set_global_opts(title_opts=opts.TitleOpts("蒙商银行资产结构情况："),
                         legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))

        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    tl.add(pie, "{}".format(it))
tl.render("timeline_pie.html")
