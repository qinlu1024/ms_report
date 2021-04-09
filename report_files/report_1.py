import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.charts import Bar, Grid, Line, Liquid, Scatter, Page, Pie, Timeline
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts import options as opts
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

org_dict = {'BSBK0002': '总行营业部', 'BSBK9901': '包头分行', 'BSBK9902': '赤峰分行', 'BSBK9903': '巴彦淖尔分行',
            'BSBK9904': '通辽分行', 'BSBK9906': '鄂尔多斯分行', 'BSBK9907': '锡林郭勒分行', 'BSBK9909': '呼伦贝尔分行',
            'BSBK9911': '呼和浩特分行', 'BSBK9912': '兴安盟分行', 'BSBK9913': '乌兰察布分行', 'BSBK9915': '乌海分行',
            'BSBK9916': '阿拉善分行', 'BSBK9918': '满洲里分行', 'BSBK9919': '二连浩特分行分行', 'BSBK9999': '蒙商银行汇总',
            'BSBK0001': '清算中心', 'BSBK0004': '数字银行', 'BSBKG014': '财务会计部',
            'BSBK9X03': '金融市场部汇总', 'BSBK9X04': '信用卡部汇总'}

# 资产负债
sql_fz_1 = "SELECT X.INDIC_KEY, X.INDIC_NAME, GEN_CHAR_DATE(X.STAT_DT) STAT_DT, " \
           "ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
           "WHERE 1=1  AND X.INDIC_TYPE = \'1\' " \
           "AND X.STAT_DT IN (DATE(\'2020-12-31\'),DATE(\'2021-03-31\')) " \
           "AND X.ORG_NUM = " + p_org + " AND X.CURR_CD = " + p_curr_cd + " " \
            "AND X.PERIOD = \'M\' " \
            "ORDER BY STAT_DT,INDIC_KEY "
# 利润
sql_fz_2 = "SELECT X.INDIC_KEY, X.INDIC_NAME, GEN_CHAR_DATE(X.STAT_DT) STAT_DT, " \
           "ROUND(X.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic X " \
           "WHERE 1=1  AND X.INDIC_TYPE = \'2\' " \
           "AND X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
           "AND X.ORG_NUM = " + p_org + " " \
           "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = \'Q\' " \
           "ORDER BY STAT_DT,INDIC_KEY "
# 衍生基础数据SQL
sql_fz_3 = "SELECT X.DISPLAY_SEQ AS INDIC_KEY, X.INDIC_NAME, GEN_CHAR_DATE(X.STAT_DT) STAT_DT, X.IND_VAL " \
           "FROM V_09_RM_REPORT_SHOP X " \
           "WHERE X.STAT_DT <= DATE(" + p_stat_dt + ")  " \
           "AND X.ORG_NUM = " + p_org + " " \
           "AND X.CURR_CD = " + p_curr_cd + "  AND X.PERIOD = " + p_peroid + " " \
           "ORDER BY STAT_DT,INDIC_KEY "

sql_indic_map = "SELECT CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR) AS INDIC_KEY,L.INDIC_NAME FROM t00_indic_list L " \
                "WHERE 1=1  "

sql_fz_jg = " SELECT T.INDIC_KEY, T.STAT_DT, ROUND(T.IND_VAL/10000,2) IND_VAL FROM T09_RM_INDIC T,T00_INDIC_LIST L " \
             "WHERE 1=1 AND T.INDIC_KEY = CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR)  AND L.TB = \'ZCFZ\'  " \
             "AND T.CURR_CD =\'HRMB\'  AND L.TB = \'ZCFZ\'  AND L.TYPE = \'A\'  AND L.NBR < \'127\' " \
             "AND T.STAT_DT <= DATE(" + p_stat_dt + ")  " \
             "AND T.ORG_NUM = " + p_org + " " \
             "AND T.CURR_CD = " + p_curr_cd + " AND T.PERIOD = " + p_peroid + " " \
             "ORDER BY STAT_DT,INDIC_KEY "

sql_fz_jg_2 = " SELECT T.INDIC_KEY, T.STAT_DT, ROUND(T.IND_VAL/10000,2) IND_VAL FROM T09_RM_INDIC T,T00_INDIC_LIST L " \
             "WHERE 1=1 AND T.INDIC_KEY = CONCAT(L.TB,\'_\',L.TYPE,\'_\',L.NBR)  AND L.TB = \'ZCFZ\'  " \
             "AND T.CURR_CD =\'HRMB\'  AND L.TB = \'ZCFZ\'  AND L.TYPE = \'B\'  AND L.NBR < \'217\' " \
             "AND T.STAT_DT <= DATE(" + p_stat_dt + ")  " \
             "AND T.ORG_NUM = " + p_org + " " \
             "AND T.CURR_CD = " + p_curr_cd + " AND T.PERIOD = " + p_peroid + " " \
             "ORDER BY STAT_DT,INDIC_KEY "
# 抓数据
data_fz_1 = pd.read_sql(sql_fz_1, engine)
data_fz_2 = pd.read_sql(sql_fz_2, engine)
data_fz_3 = pd.read_sql(sql_fz_3, engine)
data_fz_jg = pd.read_sql(sql_fz_jg, engine)
data_fz_jg_22 = pd.read_sql(sql_fz_jg_2, engine)

data_map = pd.read_sql(sql_indic_map, engine, index_col='INDIC_KEY')
data_dict = data_map.to_dict()['INDIC_NAME']

# 透视表
pd_exp_fz_1 = pd.pivot_table(data_fz_1, values='IND_VAL', index=['INDIC_KEY', 'INDIC_NAME'], columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
pd_exp_fz_2 = pd.pivot_table(data_fz_2, values='IND_VAL', index=['INDIC_KEY', 'INDIC_NAME'], columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
pd_exp_fz_3 = pd.pivot_table(data_fz_3, values='IND_VAL', index=['INDIC_KEY', 'INDIC_NAME'], columns='STAT_DT',
                             aggfunc=np.sum, fill_value=0)
pd_exp_fz_jg = pd.pivot_table(data_fz_jg, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                              aggfunc=np.sum, fill_value=0)
headers_jg = pd_exp_fz_jg.columns.tolist()
pd_exp_fz_jg_22 = pd.pivot_table(data_fz_jg_22, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                                 aggfunc=np.sum, fill_value=0)

# 重置索引
pd_exp_fz_p1 = pd_exp_fz_1.reset_index()
pd_exp_fz_p2 = pd_exp_fz_2.reset_index()
pd_exp_fz_p3 = pd_exp_fz_3.reset_index()

# 增减值
# print(pd_exp_fz_p1)
pd_exp_fz_p1['增减值'] = pd_exp_fz_p1['2021-03-31'] - pd_exp_fz_p1['2020-12-31']
pd_exp_fz_tb = pd_exp_fz_p1[['INDIC_KEY', 'INDIC_NAME', '2020-12-31', '2021-03-31', '增减值']]
# 增减幅
pd_exp_fz_pct = pd_exp_fz_p1[['2020-12-31', '2021-03-31']].pct_change(axis=1)
pd_exp_fz_pct = pd_exp_fz_pct.rename(columns={'2020-12-31': 'START_DT', '2021-03-31': 'END_DT'})
# 数据拼接
tb_1 = pd.concat([pd_exp_fz_tb, pd_exp_fz_pct], axis=1, join="inner").rename(columns={'INDIC_NAME': '科目',
                                                                                      'END_DT': '增幅'})
rs_1 = tb_1[['科目', '2020-12-31', '2021-03-31', '增减值', '增幅']]

tb_2 = pd_exp_fz_p2.rename(columns={'INDIC_NAME': '科目'})
rs_2 = tb_2[['科目', '2021-03-31']]

# 生成 资产负债-表格


def table_base_zc() -> Table:
    headers = []
    for i in rs_1.columns.tolist():
        headers.append(i)

    show_list = []
    for row in rs_1.round(2).itertuples():
        show_list.append([row[1], row[2], row[3], row[4], row[5]])
    # print(numsList)

    table_zc = Table()
    table_zc.add(headers, show_list)
    table_zc.set_global_opts(
        title_opts=ComponentTitleOpts(title="资产负债表", subtitle="（单位:万元  粒度:季度  币种:HRMB）")
    )
    return table_zc


def table_base_lr() -> Table:
    headers = []
    for i in rs_2.columns.tolist():
        headers.append(i)

    show_list = []
    for row in rs_2.round(2).itertuples():
        # print(row)
        show_list.append([row[1], row[2]])
    # print(numsList)

    table_lr = Table()
    table_lr.add(headers, show_list)
    table_lr.set_global_opts(
        title_opts=ComponentTitleOpts(title="利润表", subtitle="（单位:万元  粒度:季度  币种:HRMB）")
    )
    return table_lr


def jg_timeline() -> Timeline:
    # 初始化配置项
    pd_exp_fz_jg_2 = pd_exp_fz_jg.reset_index()
    pd_exp_fz_jg_2 = pd_exp_fz_jg_2.replace(data_dict)
    tl = Timeline(
        # 初始化配置项
        init_opts=opts.InitOpts(
            width='1220px',
            height='800px',
        )
    )
    for it in headers_jg:
        tmp = pd_exp_fz_jg_2[['INDIC_KEY', it]]
        pie = (
            Pie(

            ).add(
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
    return tl


def jg_timeline2() -> Timeline:
    # 初始化配置项
    pd_exp_fz_jg_2 = pd_exp_fz_jg_22.reset_index()
    pd_exp_fz_jg_2 = pd_exp_fz_jg_2.replace(data_dict)
    tl = Timeline(
        # 初始化配置项
        init_opts=opts.InitOpts(
            width='1220px',
            height='800px',
        )
    )
    for it in headers_jg:
        tmp = pd_exp_fz_jg_2[['INDIC_KEY', it]]
        pie = (
            Pie(

            ).add(
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
            .set_global_opts(title_opts=opts.TitleOpts("蒙商银行负债结构情况："),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )
        tl.add(pie, "{}".format(it))
    return tl


# 主要业务发展-趋势
sql_fz_ys = " SELECT T.INDIC_KEY, GEN_CHAR_DATE(T.STAT_DT) STAT_DT, ROUND(T.IND_VAL/10000,2) IND_VAL " \
            "FROM v_09_rm_report_shop T " \
             "WHERE 1=1  " \
             "AND T.CURR_CD =\'HRMB\'  AND T.FORMAT = 'WY'  AND T.PERIOD = \'M\'  " \
             "AND T.STAT_DT <= DATE(" + p_stat_dt + ")  " \
             "AND T.ORG_NUM = " + p_org + " " \
             "AND T.CURR_CD = " + p_curr_cd + "  " \
             "ORDER BY STAT_DT,INDIC_KEY "

data_fz_ys = pd.read_sql(sql_fz_ys, engine)
pd_exp_fz_ys = pd.pivot_table(data_fz_ys, values='IND_VAL', index='INDIC_KEY', columns='STAT_DT',
                              aggfunc=np.sum, fill_value=0)
headers = pd_exp_fz_ys.columns.tolist()
res_1 = pd_exp_fz_ys.reset_index()
res_1 = res_1.replace(data_dict)


def business_fz() -> Line:
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
    return ln


sql_lr_fb = " SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/100000000,2) IND_VAL FROM t09_rm_indic T  " \
            "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
            "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG)  " \
            "AND T.INDIC_KEY IN (\'ZCFZ_A_113\',\'ZCFZ_B_208\') "

data_lr_fb = pd.read_sql(sql_lr_fb, engine)
data_lr_fb_p = pd.pivot_table(data_lr_fb, values='IND_VAL', index='ORG_NUM', columns='INDIC_KEY',
                              aggfunc=np.sum, fill_value=0)
data_lr_fb_p.drop(['BSBK9999'], inplace=True)
data_lr_fb_p = data_lr_fb_p.reset_index()
data_lr_fb_p = data_lr_fb_p.replace(org_dict)


def fh_jg() -> Pie:
    p = Pie(
        init_opts=opts.InitOpts(
            width='1500px',
            height='760px',
        )
    ).add("",
          [list(z) for z in zip(data_lr_fb_p['ORG_NUM'], data_lr_fb_p['ZCFZ_A_113'])],
          radius=["1%", "60%"],
          center=["35%", "50%"]
          )\
         .add("", [list(z) for z in zip(data_lr_fb_p['ORG_NUM'], data_lr_fb_p['ZCFZ_B_208'])],
              radius=["1%", "60%"],
              center=["75%", "50%"])\
         .set_global_opts(title_opts=opts.TitleOpts(title="贷款、存款分布情况", subtitle="（单位：亿元）"),
                          legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))\
         .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%"))
    return p


sql_jg_scatter = "SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/100000000,2) IND_VAL FROM t09_rm_indic T  " \
                 "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
                 "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  AND T.ORG_LEVEL = \'3\'  " \
                 "AND T.INDIC_KEY IN (\'ZCFZ_A_113\',\'ZCFZ_B_208\') "

data_fh_cdb = pd.read_sql(sql_jg_scatter, engine)
pd_fh_cdb = pd.pivot_table(data_fh_cdb, values='IND_VAL', columns='INDIC_KEY', index='ORG_NUM',
                           aggfunc=np.sum, fill_value=0)
pd_fh_cdb.drop(['BSBK9X01'], inplace=True)
res_fh_cdb = pd_fh_cdb.reset_index()
res_fh_cdb = res_fh_cdb.replace(org_dict)


def jg_scatter() -> Scatter:
    s = Scatter().\
        add_xaxis(res_fh_cdb['ZCFZ_B_208'])\
        .add_yaxis(
        "蒙商银行",
        [list(z) for z in zip(res_fh_cdb['ZCFZ_A_113'], res_fh_cdb['ORG_NUM'])],
        label_opts=opts.LabelOpts(
            formatter=JsCode("function(params){return params.value[1] ;}")
        ),
        )\
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
    return s


sql_lr_fy = " SELECT  T.INDIC_KEY, T.ORG_NUM, ROUND(T.IND_VAL/10000,2) IND_VAL FROM t09_rm_indic T  " \
            "WHERE 1=1 AND T.STAT_DT = DATE(\'2021-03-31\')  " \
            "AND T.PERIOD = \'Q\' AND T.CURR_CD = \'HRMB\'  " \
            "AND T.ORG_NUM IN (SELECT ORG_NUM FROM T09_REPORT_ORG)  " \
            "AND T.INDIC_KEY IN (\'LR_A_101\',\'LR_B_114\',\'LR_E_124\') "

data_lr_fy = pd.read_sql(sql_lr_fy, engine)
data_lr_fy_p = pd.pivot_table(data_lr_fy, values='IND_VAL', index='ORG_NUM', columns='INDIC_KEY',
                              aggfunc=np.sum, fill_value=0)
data_lr_fy_p.drop(['BSBK9999'], inplace=True)
res_lr_fy = data_lr_fy_p.reset_index()
res_lr_fy = res_lr_fy.replace(org_dict)


def lr_fh_bar() -> Bar():
    bar = Bar(
        init_opts=opts.InitOpts(
            width='1600px',
            height='760px',
        )
    ).add_xaxis(res_lr_fy['ORG_NUM'].tolist())\
        .add_yaxis("营业收入", res_lr_fy['LR_A_101'].tolist())\
        .add_yaxis("营业支出", res_lr_fy['LR_B_114'].tolist())\
        .add_yaxis("净利润", res_lr_fy['LR_E_124'].tolist())\
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="各家分行利润分布情况", subtitle="金额：万元"),
    )
    return bar


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
pd_exp_fz_loan = pd.pivot_table(data_fz_loan, values='IND_VAL', index='GL_ACCT_NAME', columns='STAT_DT',
                                aggfunc=np.sum, fill_value=0)
headers_loan = pd_exp_fz_loan.columns.tolist()
res_fz_loan = pd_exp_fz_loan.reset_index()


def fh_daikuan_qs() -> Line():
    ln = Line(
        init_opts=opts.InitOpts(
            width='1220px',
            height='760px',
        )
    )
    ln.add_xaxis(headers_loan)
    for row in res_fz_loan.index:
        ln.add_yaxis(res_fz_loan.iloc[row, 0], res_fz_loan.iloc[row, 1:].tolist())
    ln.set_global_opts(title_opts=opts.TitleOpts(title="贷款产品发展趋势"))
    return ln


sql_fz_deb = " SELECT T.GL_ACCT_NAME, GEN_CHAR_DATE(T.STAT_DT) STAT_DT, ROUND(T.CR_BAL/10000,2) IND_VAL " \
              " FROM v_ywzk_tmp T WHERE 1=1  " \
              " AND T.STAT_DT <= DATE(" + p_stat_dt + ") " \
              " AND T.PERIOD = "+p_peroid+" " \
              " AND T.CURR_CD = " + p_curr_cd + " " \
              " AND T.ORG_NUM = " + p_org + " " \
              " AND T.GL_ACCT_LEVEL = \'1\' " \
              " AND LEFT(T.GL_ACCT,2) = \'22\' " \
              " AND T.DR_BAL = 0 "
data_fz_deb = pd.read_sql(sql_fz_deb, engine)
pd_exp_fz_deb = pd.pivot_table(data_fz_deb, values='IND_VAL', index='GL_ACCT_NAME', columns='STAT_DT',
                               aggfunc=np.sum, fill_value=0)
headers_fz_deb = pd_exp_fz_deb.columns.tolist()
res_fz_deb = pd_exp_fz_deb.reset_index()


def cp_jg() -> Line():
    ln = Line(
        init_opts=opts.InitOpts(
            width='1220px',
            height='760px',
        )
    )
    ln.add_xaxis(headers_fz_deb)
    for row in res_fz_deb.index:
        ln.add_yaxis(res_fz_deb.iloc[row, 0], res_fz_deb.iloc[row, 1:].tolist())
    ln.set_global_opts(title_opts=opts.TitleOpts(title="存款产品发展趋势"))
    return ln


def page_simple_layout():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # bar_datazoom_slider(),
        # line_markpoint(),
        # pie_rosetype(),
        # grid_mutil_yaxis(),
        # liquid_data_precision(),
        table_base_zc(),
        table_base_lr(),
        jg_scatter(),
        business_fz(),
        jg_timeline(),
        jg_timeline2(),
        fh_daikuan_qs(),
        cp_jg(),
        fh_jg(),
        lr_fh_bar(),
    )
    page.render("page_simple_layout.html")


if __name__ == "__main__":
    page_simple_layout()
