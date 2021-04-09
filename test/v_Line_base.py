import pyecharts.options as opts
from pyecharts.charts import Line
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
p_peroid = 'M'
p_org = "\'BSBK9999\'"

sql_indic_map = "SELECT CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR) AS INDIC_KEY,L.INDIC_NAME FROM t00_indic_list L " \
                "WHERE 1=1 " \

sql_fz_ys = " SELECT T.INDIC_KEY, GEN_CHAR_DATE(T.STAT_DT) STAT_DT, ROUND(T.IND_VAL/10000,2) IND_VAL " \
            "FROM v_09_rm_report_shop T " \
             "WHERE 1=1  " \
             "AND T.CURR_CD =\'HRMB\'  AND T.FORMAT = 'WY'  AND T.PERIOD = \'M\'  " \
             "AND T.STAT_DT <= DATE(" + p_stat_dt + ")  " \
             "AND T.ORG_NUM = " + p_org + " " \
             "AND T.CURR_CD = " + p_curr_cd + "  " \
             "ORDER BY STAT_DT,INDIC_KEY "

# 通过pandas读取 机构数据
data_map = pd.read_sql(sql_indic_map, engine, index_col='INDIC_KEY')
data_dict = data_map.to_dict()['INDIC_NAME']
# print(data_dict)

data_fz_ys = pd.read_sql(sql_fz_ys, engine)
pd_exp_fz_ys = pd.pivot_table(data_fz_ys, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                              aggfunc=np.sum, fill_value=0)
headers = pd_exp_fz_ys.columns.tolist()
res_1 = pd_exp_fz_ys.reset_index()
res_1 = res_1.replace(data_dict)
print(res_1)

ln = Line(
    init_opts=opts.InitOpts(
        width='1220px',
        height='760px',
    )
)
ln.add_xaxis(headers)
for row in res_1.index:
    ln.add_yaxis(res_1.iloc[row, 0], res_1.iloc[row, 1:].tolist())
ln.set_global_opts(title_opts=opts.TitleOpts(title="业务量发展趋势"))
ln.render("line_base.html")
