from pyecharts import options as opts
from pyecharts.charts import Pie, Timeline
from pyecharts.faker import Faker
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

print('-------------------------------------------------------------------------------------------------------')
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
# data_fz_1 = pd.read_sql(sql_fz_1, engine).rename(columns={'INDIC_NAME': '指标名称'})
data_map = pd.read_sql(sql_indic_map, engine, index_col='INDIC_KEY')
data_dict = data_map.to_dict()['INDIC_NAME']
print(data_dict['ZCFZ_A_101'])
data_fz_1 = pd.read_sql(sql_fz_1, engine)

pd_exp_fz_1 = pd.pivot_table(data_fz_1, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
headers = pd_exp_fz_1.columns.tolist()
pd_exp_fz_2 = pd_exp_fz_1.reset_index()
# print(pd_exp_fz_2)

tl = Timeline()
for it in headers:
    tmp = pd_exp_fz_1[it]
    tmp2 = tmp.reset_index()
    pie = (
        Pie()
        .add(
            "资产负债表",
            [list(z) for z in zip(data_dict[tmp2['INDIC_KEY']], tmp2[it])],
            rosetype="radius",
            radius=["70%", "70%"],
        )
        .set_global_opts(title_opts=opts.TitleOpts("某商店{}年营业额".format(it)))
    )
    tl.add(pie, "{}".format(it))
tl.render("timeline_pie.html")
