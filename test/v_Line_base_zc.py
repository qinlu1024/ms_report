import pyecharts.options as opts
from pyecharts.charts import Line
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
p_stat_dt = "\'2021-03-31\'"
p_curr_cd = "\'HRMB\'"
p_peroid = "\'M\'"
p_org = "\'BSBK9999\'"

sql_fz_loan = " SELECT T.GL_ACCT_NAME, GEN_CHAR_DATE(T.STAT_DT) STAT_DT, ROUND(T.DR_BAL/10000,2) IND_VAL " \
              " FROM v_ywzk_tmp T WHERE 1=1  " \
              " AND T.STAT_DT <= DATE(" + p_stat_dt + ") " \
              " AND T.PERIOD = "+p_peroid+" " \
              " AND T.CURR_CD = " + p_curr_cd + " " \
              " AND T.ORG_NUM = " + p_org + " " \
              " AND T.GL_ACCT_LEVEL = \'1\' " \
              " AND LEFT(T.GL_ACCT,2) = \'12\' " \
              " AND T.CR_BAL = 0 "
data_fz_loan = pd.read_sql(sql_fz_loan, engine)
pd_exp_fz_ys = pd.pivot_table(data_fz_loan, values='IND_VAL', index='GL_ACCT_NAME', columns='STAT_DT',
                              aggfunc=np.sum, fill_value=0)
headers = pd_exp_fz_ys.columns.tolist()
res_1 = pd_exp_fz_ys.reset_index()

ln = Line(
    init_opts=opts.InitOpts(
        width='1220px',
        height='760px',
    )
)
ln.add_xaxis(headers)
for row in res_1.index:
    ln.add_yaxis(res_1.iloc[row, 0], res_1.iloc[row, 1:].tolist())
ln.set_global_opts(title_opts=opts.TitleOpts(title="贷款产品发展趋势"))
ln.render("line_base_loan.html")
