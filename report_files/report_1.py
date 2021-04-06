import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie, Timeline
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts import options as opts

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
           "AND X.STAT_DT <= DATE(\'2021-03-31\')  " \
           "AND X.ORG_NUM = " + p_org + " AND X.CURR_CD = " + p_curr_cd + " " \
            "AND X.PERIOD = " + p_peroid + " " \
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
                "WHERE 1=1  AND TB=\'ZCFZ\'  AND IS_DISPLAY = \'1\'  ORDER BY DISPLAY_SEQ    "

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
# headers_jg_22 = pd_exp_fz_jg_22.columns.tolist()
# print(headers_jg)
# 重置索引
pd_exp_fz_p1 = pd_exp_fz_1.reset_index()
pd_exp_fz_p2 = pd_exp_fz_2.reset_index()
pd_exp_fz_p3 = pd_exp_fz_3.reset_index()

# 增减值
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

    numsList = []
    for row in rs_1.round(2).itertuples():
        # print(row)
        numsList.append([row[1], row[2], row[3], row[4], row[5]])
    # print(numsList)

    table_zc = Table()
    table_zc.add(headers, numsList)
    table_zc.set_global_opts(
        title_opts=ComponentTitleOpts(title="资产负债表", subtitle="（单位:万元  粒度:季度  币种:HRMB）")
    )
    return table_zc


def table_base_lr() -> Table:
    headers = []
    for i in rs_2.columns.tolist():
        headers.append(i)

    numsList = []
    for row in rs_2.round(2).itertuples():
        # print(row)
        numsList.append([row[1], row[2]])
    # print(numsList)

    table_lr = Table()
    table_lr.add(headers, numsList)
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
            height='900px',
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
            height='900px',
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
        jg_timeline(),
        jg_timeline2(),
    )
    page.render("page_simple_layout.html")


if __name__ == "__main__":
    page_simple_layout()
